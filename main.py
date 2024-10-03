import bpy, textwrap
from .templates import *
from .interfaces import getTemplatesFiles

### Additional panel functions

def _label_multiline(context, text, parent):
    chars = int(context.region.width / 7)   # 7 pix on 1 character
    wrapper = textwrap.TextWrapper(width=chars)
    text_lines = wrapper.wrap(text=text)
    for text_line in text_lines:
        parent.label(text=text_line)

class BlenderScriptManager:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Script Manager"

class TemplatesPanel(BlenderScriptManager, bpy.types.Panel):
    bl_label = "Custom Script Manager"
    bl_idname = "BSM_CL_Templates"
    bl_order = 0

    def draw(self, context):
        layout = self.layout
        
        ### --- GET PREFERENCES --- ###
        ###############################
        
        PREFERENCES = bpy.context.preferences.addons["BlenderScriptManager"].preferences
        
        # Set dir if not exist
        if PREFERENCES.script_dir == "":
            layout.label(text="Please set the script directory in preferences.")
            layout.operator(OpenAddonPreferencesOperator.bl_idname, text="Open Addon Preferences", icon='PREFERENCES')
            return None
        
        if context.scene.BSM_TemplatesFilesList == "":
            _label_multiline(context, "Your script folder not contain any .json template file. You must create one.", layout)
            op = layout.operator(CreateJsonFile.bl_idname, text="Create .json file", icon='ADD')
            op.path = PREFERENCES.script_dir
            op.name = "templates.json"
            layout.operator(OpenAddonPreferencesOperator.bl_idname, text="Open Addon Preferences", icon='PREFERENCES')
            return None
        
        ### --- SETUP TEMPLATES --- ###
        ###############################
        
        SETUP_Templates(context, layout)

class ExtensionPanel(BlenderScriptManager, bpy.types.Panel):
    bl_parent_id = "BSM_CL_Templates"
    bl_label = "Extensions"
    bl_options = {'DEFAULT_CLOSED'}
    
    template_index: bpy.props.IntProperty()
    
    @classmethod
    def poll(cls, context):
        data = bpy.context.preferences.addons["BlenderScriptManager"].preferences.script_dir
        if data == "":
            return False
        else:
            if context.scene.BSM_TemplatesFilesList == "":
                return False
            else:
                if len(context.scene.BSM_Templates_collection) > 0:
                    return True
                else:
                    return False
        
    
    def draw(self, context):
        layout = self.layout
        
        self.template_index = context.scene.BSM_Templates_collection.find(context.workspace.BSM_Templates)
        
        DRAW_Extensions(context, layout, self.template_index)

class ScriptsPanel(BlenderScriptManager, bpy.types.Panel):
    bl_parent_id = "BSM_CL_Templates"
    bl_label = "Scripts"
    
    template_index: bpy.props.IntProperty()
    script_index: bpy.props.IntProperty()
    
    @classmethod
    def poll(cls, context):
        data = bpy.context.preferences.addons["BlenderScriptManager"].preferences.script_dir
        if data == "":
            return False
        else:
            if context.scene.BSM_TemplatesFilesList == "":
                return False
            else:
                if len(context.scene.BSM_Templates_collection) > 0:
                    return True
                else:
                    return False

    def draw(self, context):
        
        self.template_index = context.scene.BSM_Templates_collection.find(context.workspace.BSM_Templates)
        
        layout = self.layout
        
        if len(context.scene.BSM_Templates_collection) != 0:
            if len(context.scene.BSM_Templates_collection[self.template_index].scripts) != 0:
                for script in context.scene.BSM_Templates_collection[self.template_index].scripts:
                    
                    box = layout.box()
                    
                    ### --- SUBPANEL --- ###
                    
                    panel_row = box.row()
                    icon = 'TRIA_DOWN' if script.status else 'TRIA_RIGHT'
                    panel_row.prop(script, "status", icon=icon, icon_only=True)
                    
                    ########################
                    
                    self.script_index = context.scene.BSM_Templates_collection[self.template_index].scripts.find(script.name)
                    
                    if script.status: 
                        
                        ### ---   ARGS LAYOUTS  --- ###
                        DRAW_Arguments(context, script, box, self.template_index, self.script_index)
                            
                        op = box.operator("args.add_item", text="Add Argument", icon="ADD")
                        op.template_index = self.template_index
                        op.script_index = self.script_index
                        
                        ###############################
                    
                    EXECUTE_Script(panel_row, script)
                    
                        
                    op = panel_row.operator("scripts.edit_item", text="", icon="GREASEPENCIL")
                    op.template_index = self.template_index
                    op.script_index = self.script_index
                    op.name = script.name
                    op.description = script.description
                    op.icon = script.icon
                    op.path = script.path
                    
                    op = panel_row.operator("scripts.remove_item", text="", icon="REMOVE")
                    op.template_index = self.template_index
                    op.script_index = self.script_index

            op = layout.operator("scripts.add_item", text="", icon="ADD")
            op.template_index = self.template_index
            return None
            
        op = layout.label(text="You need template to add any scripts.")

class Settings(BlenderScriptManager, bpy.types.Panel):
    bl_parent_id = "BSM_CL_Templates"
    bl_label = "Settings"
    
    @classmethod
    def poll(cls, context):
        data = bpy.context.preferences.addons["BlenderScriptManager"].preferences.script_dir
        if data == "":
            return False
        else:
            if context.scene.BSM_TemplatesFilesList == "":
                return False
            else:
                return True

    def draw(self, context):
        
        PREFERENCES = bpy.context.preferences.addons["BlenderScriptManager"].preferences
        
        layout = self.layout
        
        box = layout.box()
        
        row = box.row()
        row.prop(context.scene, "BSM_TemplatesFilesList", text="")
        
        edit = row.operator("template.edit_file", text="", icon='TOOL_SETTINGS')
        edit.path = context.scene.BSM_TemplatesFilesList
        file_name = context.scene.BSM_TemplatesFilesList
        edit.template_file_name = file_name[0:file_name.find(".json")]
        
        add_new = row.operator(CreateJsonFile.bl_idname, text="", icon='ADD')
        add_new.path = PREFERENCES.script_dir
        add_new.name = "templates.json"
        
        del_new = row.operator(DeleteJsonFile.bl_idname, text="", icon='REMOVE')
        del_new.path = PREFERENCES.script_dir
        del_new.name = context.scene.BSM_TemplatesFilesList
        
        if len(context.scene.BSM_Templates_collection) == 0:
            box.operator(LoadTemplates.bl_idname, text="Load Templates", icon="IMPORT")
        
        layout.operator(OpenAddonPreferencesOperator.bl_idname, text="Open Addon Preferences", icon='PREFERENCES')
        
    
MainClasses = [
    TemplatesPanel,
    ExtensionPanel,
    ScriptsPanel,
    Settings,
]

def MainProps():
    
    bpy.types.Scene.BSM_TemplatesFilesList = bpy.props.EnumProperty(name="Templates Files", items=getTemplatesFiles, update=clearProperties)
    
    bpy.types.Scene.BSM_TemplatesFilesList_collection = bpy.props.CollectionProperty(type=Files)

def delMainProps():
    
    del bpy.types.Scene.BSM_TemplatesFilesList
    
def clearMainProps():
    pass
