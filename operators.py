import bpy
import importlib.util

from .defers import *
from .interfaces import *

# Operator to open the add-on preferences
class OpenAddonPreferencesOperator(bpy.types.Operator):
    bl_idname = "wm.open_addon_prefs"
    bl_label = "Open Addon Preferences"
    
    def execute(self, context):
        # Open the Add-ons preferences tab
        bpy.ops.screen.userpref_show('INVOKE_DEFAULT')
        bpy.context.preferences.active_section = 'ADDONS'
        bpy.data.window_managers['WinMan'].addon_search = "Custom Script Manager"
        bpy.ops.preferences.addon_expand(module = "BlenderScriptManager")
        return {'FINISHED'}

class LoadTemplates(bpy.types.Operator):
    bl_idname = "wm.load_templates"
    bl_label = "Load Template"
    
    def execute(self, context):
        # Get the file name from the addon preferences
        PREFERENCES = bpy.context.preferences.addons["BlenderScriptManager"].preferences

        layout = self.layout

        script_dir = PREFERENCES.script_dir
        templates_list = PREFERENCES.templates_list
        templates_list = jsonImport(script_dir, "templates.json")
        templates_list = templates_list['templates']
        
        context.scene.templates_collection.clear()
        
        # Get List Item Index
        template_index = 0
        script_index = 0
        
        for template in templates_list:
            addTemplate(context, template['name'])
            for script in template['scripts']:
                status = True if script["status"] == 1 else False
                addScript(context, template_index, 
                          script['name'], 
                          script['description'], 
                          script['icon'], 
                          script['path'], 
                          status)
                for arg in script['args']:
                    addArgs(context, template_index, script_index,
                          arg['type'], 
                          arg['name'], 
                          arg['description'], 
                          arg['value'])
                
                script_index = script_index + 1 # Increment Index 
            
            script_index = 0
            template_index = template_index + 1 # Increment Index 
                    
                
        context.scene.isSave = False
        

        return {'FINISHED'}

class SaveTemplates(bpy.types.Operator):
    bl_idname = "wm.save_templates"
    bl_label = "Save Template"
    
    def execute(self, context):
        # Get the file name from the addon preferences
        preferences = bpy.context.preferences.addons["BlenderScriptManager"].preferences

        jsonExport(preferences.script_dir, 'templates.json', serializeDict(context.scene.templates_collection))

        context.scene.isSave = False

        return {'FINISHED'}

class RunScriptsOperator(bpy.types.Operator):
    bl_idname = "wm.run_scripts_operator"
    bl_label = "Run Scripts in Directory"

    script_dir: bpy.props.StringProperty(name="Script Dir", default="")
    script_name: bpy.props.StringProperty(name="Script Name", default="")
    
    props: bpy.props.CollectionProperty(type=Args)
    
    def execute(self, context):
        filepath = self.script_dir + self.script_name

        self.run_script(filepath)
        
        self.report({'INFO'}, "Scripts executed")
        return {'FINISHED'}
    
    def run_script(self, filepath):
        # Dynamically import and execute the script
        spec = importlib.util.spec_from_file_location("module.name", filepath)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Init Props value for script
        args = {}
        for prop in self.props:
            # Basic Properties or Cusom Object Properties
            key = getVarType(var_types, prop.type)[0]
            
            value = prop[key]
            
            prop_name = prop.name
            
            if "CUSTOM" in prop.type:
                sub_args = {}
                
                if prop.type == "CUSTOM":
                    target_object = bpy.context.scene.objects.get(value)
                if prop.type == "CUSTOM_SELF":
                    target_object = bpy.context.active_object
                    
                for prop_item in target_object.keys():
                    ignore_mask = prop_item + ";"
                    if ignore_mask not in prop.name:
                        if prop_item != "_RNA_UI":
                            sub_args.update({prop_item: target_object[prop_item]})
                
                value = sub_args
                prop_name = target_object.name
                
            
            args.update({prop_name: value})
            
        # Assuming there's a function named 'main' in each script
        if hasattr(module, "main"):
            try:                
                module.main(args)  # Execute the 'main' function
            except Exception as e:
                print(f"Error running main() in {filepath}: {e}")

    
OperatorsClasses = [
    OpenAddonPreferencesOperator,
    LoadTemplates,
    SaveTemplates,
    RunScriptsOperator
]