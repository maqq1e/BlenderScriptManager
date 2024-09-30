import bpy

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

class CreateJsonFile(bpy.types.Operator):
    bl_idname = "wm.create_json_file"
    bl_label = "Create new .json template file?"
    
    path: bpy.props.StringProperty(name="Path", default="")
    name: bpy.props.StringProperty(name="Name", default="")
    
    def execute(self, context):
        
        data = {
            "templates": [],
            "extensions": []
        }
        
        if not checkFileExist(self.path, self.name):
            jsonExport(self.path, self.name, data)
        else:
            jsonExport(self.path, "1_" + self.name, data)
        return {'FINISHED'}
    
    def invoke(self, context, event):

        return context.window_manager.invoke_confirm(self, event)

class DeleteJsonFile(bpy.types.Operator):
    bl_idname = "wm.delete_json_file"
    bl_label = "Delete current .json template file?"
    
    path: bpy.props.StringProperty(name="Path", default="")
    name: bpy.props.StringProperty(name="Name", default="")
    
    def execute(self, context):
        
        deleteFile(self.path, self.name)
        
        return {'FINISHED'}

    
    def invoke(self, context, event):

        return context.window_manager.invoke_confirm(self, event)

class LoadTemplates(bpy.types.Operator):
    bl_idname = "wm.load_templates"
    bl_label = "Load Template"
    
    def execute(self, context):
        # Get the file name from the addon preferences
        PREFERENCES = bpy.context.preferences.addons["BlenderScriptManager"].preferences

        script_dir = PREFERENCES.script_dir
        templates_name = context.scene.BSM_TemplatesFilesList
        templates_list = jsonImport(script_dir, templates_name)
        extensions_list = templates_list['extensions']
        templates_list = templates_list['templates']
        
        context.scene.templates_collection.clear()
        context.scene.extensions_collection.clear()
        
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
            
            for extension in template['extensions']:
                addExtension(context, template_index,
                             extension['name'])
            
            script_index = 0
            template_index = template_index + 1 # Increment Index 
        # print(extensions_list[0])
        for ext in extensions_list:
            addGlobalExtension(context, ext['name'])
        
        context.scene.isSave = False
        

        return {'FINISHED'}

class SaveTemplates(bpy.types.Operator):
    bl_idname = "wm.save_templates"
    bl_label = "Save Template"
    
    def execute(self, context):
        # Get the file name from the addon preferences
        preferences = bpy.context.preferences.addons["BlenderScriptManager"].preferences
        
        templates = context.scene.templates_collection
        extensions = context.scene.extensions_collection

        jsonExport(preferences.script_dir, 'templates.json', serializeDict(templates, extensions))

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

        status = executeScript(self.props, filepath)
        
        self.report(status[0], status[1])
        return {'FINISHED'}

class RegisterScriptOperator(bpy.types.Operator):
    bl_idname = "wm.register_script_operator"
    bl_label = "Register Script from Directory"

    script_dir: bpy.props.StringProperty(name="Script Dir", default="")
    script_name: bpy.props.StringProperty(name="Script Name", default="")
    
    template_name: bpy.props.StringProperty()
    
    isUnregister: bpy.props.BoolProperty(default=False)
    
    def execute(self, context):

        registerClass(self.script_dir, self.script_name, self.isUnregister)
        changeExtensionStatus(context, self.template_name, self.script_name)
        
        context.scene.isSave = True
        
        return {'FINISHED'}
    
OperatorsClasses = [
    OpenAddonPreferencesOperator,
    LoadTemplates,
    SaveTemplates,
    RunScriptsOperator,
    RegisterScriptOperator,
    CreateJsonFile,
    DeleteJsonFile
]