import bpy
import importlib.util
from .defers import jsonImport, addTemplate, addScript, addArgs, jsonExport, serializeDict, getVarType
from .GLOBAL import var_types, var_types_options

from .TemplatesEnum import TemplateClasses, TemplateProps, delTemplateProps, Args

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

class InfoTab(bpy.types.Panel):
    bl_label = "Script Manager"
    bl_idname = "OBJECT_PT_custom_scripts_manager"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Script Manager"

    def draw(self, context):
        ### --- GET PREFERENCES --- ###
        ###############################
        
        # Get the file name from the addon preferences
        preferences = bpy.context.preferences.addons["BlenderScriptManager"].preferences

        # Set dir if not exist
        if preferences.script_dir == "":
            layout.label(text="Please set the script directory in preferences.")
            layout.operator(OpenAddonPreferencesOperator.bl_idname, text="Open Addon Preferences", icon='PREFERENCES')
            return None
        
        ### --- SETUP TEMPLATES --- ###
        ###############################
        
        layout = self.layout
        
        row = layout.row(align=True)
        # If Templates changed
        if context.scene.isSave:
            row.enabled = True
        else:
            row.enabled = False
        row.operator(LoadTemplates.bl_idname, text="Revert Changes", icon="LOOP_BACK")
        row.operator(SaveTemplates.bl_idname, text="Save Templates", icon="EXPORT")
        
        row = layout.row(align=True)
        row.prop(context.scene, "Templates", text="")
        row.operator("templates.add_item", text="", icon="ADD")
        op = row.operator("templates.remove_item", text="", icon="REMOVE")

        if len(context.scene.templates_collection) == 0:
            layout.label(text="You need to create your first template")
            layout.operator(LoadTemplates.bl_idname, text="Load Templates", icon="IMPORT")
            return None
        
        template_index = context.scene.templates_collection.find(context.scene.Templates)
        op.index = template_index

        layout.prop(context.scene.templates_collection[context.scene.Templates], "name", text="Template Name: ")

        ### --- SCRIPTS LAYOUTS --- ###
        ###############################

        if len(context.scene.templates_collection[template_index].scripts) != 0:
            for script in context.scene.templates_collection[template_index].scripts:
                
                box = layout.box()
                
                ### --- SUBPANEL --- ###
                
                panel_row = box.row()
                icon = 'TRIA_DOWN' if script.status else 'TRIA_RIGHT'
                panel_row.prop(script, "status", icon=icon, icon_only=True)
                
                ########################
                
                script_index = context.scene.templates_collection[template_index].scripts.find(script.name)
                
                if script.status: 
                    
                    ### ---   ARGS LAYOUTS  --- ###
                    
                    for arg in script.args:
                        arg_index = script.args.find(arg.name)
                        
                        box.separator(factor=0.3, type="LINE")
                           
                        args_row = box.row()
                                                                        
                        varType = getVarType(var_types, arg.type)
                        key = varType[0]
                        index = varType[1]
                        option = var_types_options[index]
                        
                        ### ---   CUSTOM OBJECT PROPERTIES   --- ###
                        if "CUSTOM" in arg.type:
                            
                            if arg.type == "CUSTOM":
                                target_object = context.scene.objects.get(arg.custom)
                            if arg.type == "CUSTOM_SELF":
                                target_object = context.active_object
                                if target_object == None:
                                    continue
                            
                            prop_box = args_row.box()
                            prop_row = prop_box.grid_flow()
                            
                            _props_count = 0
                                                        
                            for prop in target_object.keys():
                                ignore_mask = prop + ";"
                                if ignore_mask not in arg.name:
                                    if prop != "_RNA_UI":  # Ignore the '_RNA_UI' entry
                                        prop_row.prop(target_object, f'["{prop}"]', text=prop)
                                        _props_count = _props_count + 1
                            
                            if (_props_count == 0):
                                prop_row.label(text="You have no any properties.")
                        ###############################################
                        else:
                            args_row.prop(arg, key, text="" if option['hideName'] else arg.name, 
                                        slider=option['slider'],
                                        toggle=option['toggle'],
                                        icon_only=option['icon_only']
                                        )
                        
                        op = args_row.operator("args.edit_item", text="", icon="TOOL_SETTINGS")
                        op.template_index = template_index
                        op.script_index = script_index
                        op.arg_index = arg_index
                        op.name = arg.name
                        op.description = arg.description
                        op.type = arg.type
                        _value = op.value.add()
                        _value[key] = arg[key]
                        
                        op = args_row.operator("args.remove_item", text="", icon="REMOVE")
                        op.template_index = template_index
                        op.script_index = script_index
                        op.arg_index = arg_index
                        
                    op = box.operator("args.add_item", text="Add Argument", icon="ADD")
                    op.template_index = template_index
                    op.script_index = script_index
                    
                    ###############################
                    
                op = panel_row.operator(RunScriptsOperator.bl_idname, text=script.name, icon=script.icon)
                op.script_dir = preferences.script_dir
                op.script_name = script.path # Path is name of script
                for arg in script.args:
                    ap = op.props.add()
                    ap.name = arg.name
                    ap.description = arg.description
                    ap.type = arg.type
                    
                    key = getVarType(var_types, arg.type)[0]
                    
                    ap[key] = arg[key]
                    
                op = panel_row.operator("scripts.edit_item", text="", icon="GREASEPENCIL")
                op.template_index = template_index
                op.script_index = script_index
                op.name = script.name
                op.description = script.description
                op.icon = script.icon
                op.path = script.path
                
                op = panel_row.operator("scripts.remove_item", text="", icon="REMOVE")
                op.template_index = template_index
                op.script_index = script_index


        op = layout.operator("scripts.add_item", text="", icon="ADD")
        op.template_index = template_index

class LoadTemplates(bpy.types.Operator):
    bl_idname = "wm.load_templates"
    bl_label = "Load Template"
    
    def execute(self, context):
        # Get the file name from the addon preferences
        preferences = bpy.context.preferences.addons["BlenderScriptManager"].preferences

        layout = self.layout

        script_dir = preferences.script_dir
        templates_list = preferences.templates_list
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

### --- CUSTOM SCRIPTS EXECUTE --- ###
######################################

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
        

UsesClasses = [
    Args, # Need to refactory!
    InfoTab,
    OpenAddonPreferencesOperator,
    RunScriptsOperator,
    LoadTemplates,
    SaveTemplates
]

UsesClasses.extend(TemplateClasses)

def MainProps():

    TemplateProps()


def delMainProps():

    delTemplateProps()
