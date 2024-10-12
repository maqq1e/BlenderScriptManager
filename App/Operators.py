import bpy
from enum import Enum

from .Interfaces import *
from ..Defers.Control import *

class OPERATORS(Enum):
    open_addon_prefs = "operators.open_addon_prefs"
    create_json_file = "operators.create_json_file"
    delete_json_file = "operators.delete_json_file"
    load_templates = "operators.load_templates"
    save_templates = "operators.save_templates"
    run_scripts = "operators.run_scripts"
    register_script = "operators.register_script"
    edit_template_file = "operators.edit_template_file"

# Operator to open the add-on preferences
class OPERATOR_OpenAddonPreferencesOperator(bpy.types.Operator):
    bl_idname = OPERATORS.open_addon_prefs.value
    bl_label = "Open Addon Preferences"
    
    def execute(self, context):
        # Open the Add-ons preferences tab
        bpy.ops.screen.userpref_show('INVOKE_DEFAULT')
        bpy.context.preferences.active_section = 'ADDONS'
        bpy.data.window_managers['WinMan'].addon_search = "Custom Script Manager"
        bpy.ops.preferences.addon_expand(module = "BlenderScriptManager")
        return {'FINISHED'}

class OPERATOR_CreateJsonFile(bpy.types.Operator):
    bl_idname = OPERATORS.create_json_file.value
    bl_label = "Create new .json template file?"
    
    path: bpy.props.StringProperty(name="Path", default="")
    name: bpy.props.StringProperty(name="Name", default="")
    
    def execute(self, context):
        
        data = {
            "templates": [],
            "extensions": []
        }
        
        if not EXT_checkFileExist(self.path, self.name):
            EXT_jsonExport(self.path, self.name, data, True)
        else:
            EXT_jsonExport(self.path, "1_" + self.name, data, True)
            
    
        return {'FINISHED'}
    
    def invoke(self, context, event):

        return context.window_manager.invoke_confirm(self, event)

class OPERATOR_DeleteJsonFile(bpy.types.Operator):
    bl_idname = OPERATORS.delete_json_file.value
    bl_label = "Delete current .json template file?"
    
    path: bpy.props.StringProperty(name="Path", default="")
    name: bpy.props.StringProperty(name="Name", default="")
    
    def execute(self, context):
        
        EXT_deleteFile(self.path, self.name)
        
        return {'FINISHED'}

    
    def invoke(self, context, event):

        return context.window_manager.invoke_confirm(self, event)

class OPERATOR_LoadTemplates(bpy.types.Operator):
    bl_idname = OPERATORS.load_templates.value
    bl_label = "Load Template"
    
    def execute(self, context):
        
        EXT_loadDatas(self, context)        

        return {'FINISHED'}
    
    def invoke(self, context, event):

        return context.window_manager.invoke_confirm(self, event)

class OPERATOR_SaveTemplates(bpy.types.Operator):
    bl_idname = OPERATORS.save_templates.value
    bl_label = "Save Template"
    
    def execute(self, context):
        # Get the file name from the addon preferences
        preferences = bpy.context.preferences.addons["BlenderScriptManager"].preferences
        
        templates = context.scene.BSM_Templates_collection
        extensions = context.scene.BSM_Extensions_collection
        
        file = context.scene.BSM_TemplatesFilesList

        EXT_jsonExport(preferences.script_dir, file, EXT_serializeDict(templates, extensions))

        context.scene.BSM_isSave = False

        return {'FINISHED'}

class OPERATOR_RunScriptsOperator(bpy.types.Operator):
    bl_idname = OPERATORS.run_scripts.value
    bl_label = "Run Scripts in Directory"

    script_dir: bpy.props.StringProperty(name="Script Dir", default="")
    script_name: bpy.props.StringProperty(name="Script Name", default="")
    
    props: bpy.props.CollectionProperty(type=INTERFACE_Args)
    
    def execute(self, context):
        filepath = self.script_dir + self.script_name

        status = EXT_executeScript(self.props, filepath)
        
        self.report(status[0], status[1])
        return {'FINISHED'}

class OPERATOR_RegisterScriptOperator(bpy.types.Operator):
    bl_idname = OPERATORS.register_script.value
    bl_label = "Register Script from Directory"

    script_dir: bpy.props.StringProperty(name="Script Dir", default="")
    script_name: bpy.props.StringProperty(name="Script Name", default="")
    
    template_name: bpy.props.StringProperty()
    
    isUnregister: bpy.props.BoolProperty(default=False)
    
    def execute(self, context):

        EXT_registerClass(self.script_dir, self.script_name, self.isUnregister)
        CMP_changeExtensionStatus(context, self.template_name, self.script_name)
        
        context.scene.BSM_isSave = True
        
        return {'FINISHED'}

class OPERATOR_EditTemplateFileOperator(bpy.types.Operator):
    bl_idname = OPERATORS.edit_template_file.value
    bl_label = "Edit Template File"
    
    template_file_name: bpy.props.StringProperty(name="Name")

    new_name: bpy.props.StringProperty(name="Name")

    path: bpy.props.StringProperty(name="Description")
    
    def execute(self, context):
        
        EXT_renameFile(self.path, self.template_file_name, self.new_name, ".json")

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

OPERATORS_Classes = [
    OPERATOR_OpenAddonPreferencesOperator,
    OPERATOR_LoadTemplates,
    OPERATOR_SaveTemplates,
    OPERATOR_RunScriptsOperator,
    OPERATOR_RegisterScriptOperator,
    OPERATOR_CreateJsonFile,
    OPERATOR_DeleteJsonFile,
    OPERATOR_EditTemplateFileOperator
]