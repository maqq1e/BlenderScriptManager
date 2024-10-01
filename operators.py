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
        
        loadDatas(self, context)        

        return {'FINISHED'}
    
    def invoke(self, context, event):

        return context.window_manager.invoke_confirm(self, event)

class SaveTemplates(bpy.types.Operator):
    bl_idname = "wm.save_templates"
    bl_label = "Save Template"
    
    def execute(self, context):
        # Get the file name from the addon preferences
        preferences = bpy.context.preferences.addons["BlenderScriptManager"].preferences
        
        templates = context.scene.BSM_Templates_collection
        extensions = context.scene.BSM_Extensions_collection
        
        file = context.scene.BSM_TemplatesFilesList

        jsonExport(preferences.script_dir, file, serializeDict(templates, extensions))

        context.scene.BSM_isSave = False

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
        
        context.scene.BSM_isSave = True
        
        return {'FINISHED'}

class EditTemplateFileOperator(bpy.types.Operator):
    bl_idname = "template.edit_file"
    bl_label = "Edit Template File"
    
    template_file_name: bpy.props.StringProperty(name="Name")

    new_name: bpy.props.StringProperty(name="Name")

    path: bpy.props.StringProperty(name="Description")
    
    def execute(self, context):
        
        renameFile(self.path, self.template_file_name, self.new_name, ".json")

        return {'FINISHED'}
    
    def draw(self, context):
        
        layout = self.layout
        
        disbox = layout.box()
        disbox.prop(self, "template_file_name", text="Old Name")
        disbox.enabled = False
        
        box = layout.box()        
        box.prop(self, "new_name", text="New name")        
    
    def invoke(self, context, event):

        return context.window_manager.invoke_props_dialog(self)

OperatorsClasses = [
    OpenAddonPreferencesOperator,
    LoadTemplates,
    SaveTemplates,
    RunScriptsOperator,
    RegisterScriptOperator,
    CreateJsonFile,
    DeleteJsonFile,
    EditTemplateFileOperator
]