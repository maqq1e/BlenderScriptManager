import bpy

from .Defers.Control import *
from .Defers.Layouts import LAYOUT_multiline, getPreferences

from .App.Operators import OPERATORS
from .App.Interfaces import *

from .App.Datas import TEMPLATES, EXTENSIONS

def EXCEPTION_isReady(data, context):
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

class BlenderScriptManager:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Script Manager"

class TemplatesPanel(BlenderScriptManager, bpy.types.Panel):
    bl_label = "Custom Script Manager"
    bl_idname = "BSM_PT_Templates"
    bl_order = 0

    def draw(self, context):
        layout = self.layout
        
        PREFERENCES = getPreferences()
        
        ### --- GET PREFERENCES --- ###
        ###############################
        
        if PREFERENCES.script_dir == "":
            layout.label(text="Please set the script directory in preferences.")
            layout.operator(OPERATORS.open_addon_prefs.value, text="Open Addon Preferences", icon='PREFERENCES')
            return None
        
        if context.scene.BSM_TemplatesFilesList == "":
            LAYOUT_multiline(context, "Your script folder not contain any .json template file. You must create one.", layout)
            op = layout.operator(OPERATORS.create_json_file.value, text="Create .json file", icon='ADD')
            op.path = PREFERENCES.script_dir
            op.name = "templates.json"
            layout.operator(OPERATORS.open_addon_prefs.value, text="Open Addon Preferences", icon='PREFERENCES')
            return None
        
        ### --- SETUP TEMPLATES --- ###
        ###############################
        
        ### Save and Load Row
        first_row = layout.row()
        
        # If Templates changed
        if context.scene.BSM_isSave:
            first_row.enabled = True
        else:
            first_row.enabled = False
        
        ### Save and Load Buttons
        first_row.operator(OPERATORS.load_templates.value, text="Revert Changes", icon="LOOP_BACK")
        first_row.operator(OPERATORS.save_templates.value, text="Save Templates", icon="EXPORT")
        
        ### Templates Enum Row
        second_row = layout.row()
        second_row.prop(context.workspace, "BSM_Templates", text="")
        
        op = second_row.operator(TEMPLATES.templates_edit_item.value, text="", icon="TOOL_SETTINGS")
        op.old_name = context.workspace.BSM_Templates
        
        second_row.operator(TEMPLATES.templates_add_item.value, text="", icon="ADD")
        
        _delete_row = second_row.row()
        op = _delete_row.operator(TEMPLATES.templates_remove_item.value, text="", icon="REMOVE")
        
        ### If there is not any of templates
        if len(context.scene.BSM_Templates_collection) == 0:
            _delete_row.enabled = False
            layout.label(text="You need to create your first template")
            return None
        
        template_index = context.scene.BSM_Templates_collection.find(context.workspace.BSM_Templates) # Get Current Template Index
        op.index = template_index

class ExtensionPanel(BlenderScriptManager, bpy.types.Panel):
    bl_parent_id = "BSM_PT_Templates"
    bl_idname = "BSM_PT_Extensions"
    bl_label = "Extensions"
    bl_options = {'DEFAULT_CLOSED'}
        
    @classmethod
    def poll(cls, context):
        PREFERENCES = getPreferences()
        data = PREFERENCES.script_dir
        return EXCEPTION_isReady(data, context)
        
    
    def draw(self, context):
        layout = self.layout
        
        PREFERENCES = getPreferences()
        
        template_index = context.scene.BSM_Templates_collection.find(context.workspace.BSM_Templates)
        
        current_template = context.workspace.BSM_Templates
        extensions_collection = context.scene.BSM_Extensions_collection
        
        ### Iterate Extensions List
        if len(extensions_collection) != 0:
            ext_index = 0
            for ext in extensions_collection:
                box = layout.box()
                row = box.row()

                if ext.status:
                    pause_op = row.operator(OPERATORS.register_script.value, text="", icon="PAUSE", depress=True)
                    pause_op.script_dir = PREFERENCES.script_dir
                    pause_op.script_name = ext.name
                    pause_op.template_name = current_template
                    pause_op.isUnregister = True
                else:
                    op = row.operator(OPERATORS.register_script.value, text="", icon="PLAY")
                    op.script_dir = PREFERENCES.script_dir
                    op.script_name = ext.name
                    op.template_name = current_template
                    op.isUnregister = False
                
                row.label(text=ext.name)
                
                del_op = row.operator(EXTENSIONS.extensions_remove_item.value, text="", icon="REMOVE")
                del_op.template_index = template_index
                del_op.extension_index = ext_index
                
                ext_index = ext_index + 1
        else:
            layout.label(text="You have no any extensions.")
            
        layout.operator(EXTENSIONS.extensions_add_item.value, text="Add Extension")

class ScriptsPanel(BlenderScriptManager, bpy.types.Panel):
    bl_parent_id = "BSM_PT_Templates"
    bl_idname = "BSM_PT_Scripts"
    bl_label = "Scripts"
        
    @classmethod
    def poll(cls, context):
        PREFERENCES = getPreferences()
        data = PREFERENCES.script_dir
        return EXCEPTION_isReady(data, context)

    def draw(self, context):
        
        PREFERENCES = getPreferences()
        
        template_index = context.scene.BSM_Templates_collection.find(context.workspace.BSM_Templates)
        
        layout = self.layout
        
        ### Iterate Scripts
        if len(context.scene.BSM_Templates_collection) != 0:
            if len(context.scene.BSM_Templates_collection[template_index].scripts) != 0:
                for script in context.scene.BSM_Templates_collection[template_index].scripts:
                    
                    box = layout.box()
                    
                    ### --- SUBPANEL --- ###
                    
                    panel_row = box.row()
                    icon = 'TRIA_DOWN' if script.status else 'TRIA_RIGHT'
                    panel_row.prop(script, "status", icon=icon, icon_only=True)
                    
                    ########################
                    
                    script_index = context.scene.BSM_Templates_collection[template_index].scripts.find(script.name)
                    
                    if script.status: 
                        
                        ### ---   ARGS LAYOUTS  --- ###
                        for arg in script.args:
                            arg_index = script.args.find(arg.name)
                            
                            box.separator(factor=0.3, type="LINE")
                                
                            args_row = box.row()
                                                                            
                            varType = EXT_getVarType(PROPERTY_var_types, arg.type)
                            key = varType[0]
                            index = varType[1]
                            option = PROPERTY_var_types_options[index]
                            
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
                            
                            op = args_row.operator(TEMPLATES.args_edit_item.value, text="", icon="TOOL_SETTINGS")
                            op.template_index = template_index
                            op.script_index = script_index
                            op.arg_index = arg_index
                            op.name = arg.name
                            op.description = arg.description
                            op.type = arg.type
                            _value = op.value.add()
                            _value[key] = arg[key]
                            
                            op = args_row.operator(TEMPLATES.args_remove_item.value, text="", icon="REMOVE")
                            op.template_index = template_index
                            op.script_index = script_index
                            op.arg_index = arg_index
                            
                        op = box.operator(TEMPLATES.args_add_item.value, text="Add Argument", icon="ADD")
                        op.template_index = template_index
                        op.script_index = script_index
                        
                        ###############################
                                        
                    op = panel_row.operator(OPERATORS.run_scripts.value, text=script.name, icon=script.icon)
                    op.script_dir = PREFERENCES.script_dir
                    op.script_name = script.path # Path is name of script
                    for arg in script.args:
                        ap = op.props.add()
                        ap.name = arg.name
                        ap.description = arg.description
                        ap.type = arg.type
                        
                        key = EXT_getVarType(PROPERTY_var_types, arg.type)[0]
                        
                        ap[key] = arg[key]
                    
                        
                    op = panel_row.operator(TEMPLATES.scripts_edit_item.value, text="", icon="GREASEPENCIL")
                    op.template_index = template_index
                    op.script_index = script_index
                    op.name = script.name
                    op.description = script.description
                    op.icon = script.icon
                    op.path = script.path
                    
                    op = panel_row.operator(TEMPLATES.scripts_remove_item.value, text="", icon="REMOVE")
                    op.template_index = template_index
                    op.script_index = script_index

            op = layout.operator(TEMPLATES.scripts_add_item.value, text="", icon="ADD")
            op.template_index = template_index
            return None
            
        op = layout.label(text="You need template to add any scripts.")

class Settings(BlenderScriptManager, bpy.types.Panel):
    bl_parent_id = "BSM_PT_Templates"
    bl_idname = "BSM_PT_Settings"
    bl_label = "Settings"
    
    @classmethod
    def poll(cls, context):
        PREFERENCES = getPreferences()
        data = PREFERENCES.script_dir
        if data == "":
            return False
        else:
            if context.scene.BSM_TemplatesFilesList == "":
                return False
            else:
                return True

    def draw(self, context):
        PREFERENCES = getPreferences()
        
        layout = self.layout
        
        box = layout.box()
        
        row = box.row()
        row.prop(context.scene, "BSM_TemplatesFilesList", text="")
        
        edit = row.operator(OPERATORS.edit_template_file.value, text="", icon='TOOL_SETTINGS')
        edit.path = PREFERENCES.script_dir
        file_name = context.scene.BSM_TemplatesFilesList
        edit.template_file_name = file_name[0:file_name.find(".json")]
        
        add_new = row.operator(OPERATORS.create_json_file.value, text="", icon='ADD')
        add_new.path = PREFERENCES.script_dir
        add_new.name = "templates.json"
        
        del_new = row.operator(OPERATORS.delete_json_file.value, text="", icon='REMOVE')
        del_new.path = PREFERENCES.script_dir
        del_new.name = context.scene.BSM_TemplatesFilesList
        
        if len(context.scene.BSM_Templates_collection) == 0:
            box.operator(OPERATORS.load_templates.value, text="Load Templates", icon="IMPORT")
        
        layout.operator(OPERATORS.open_addon_prefs.value, text="Open Addon Preferences", icon='PREFERENCES')

MAIN_Classes = [
    TemplatesPanel,
    ExtensionPanel,
    ScriptsPanel,
    Settings,
]

def MAIN_Props():
    
    bpy.types.Scene.BSM_TemplatesFilesList = bpy.props.EnumProperty(name="Templates Files", items=getTemplatesFiles, update=EXT_clearProperties)
    
    bpy.types.Scene.BSM_TemplatesFilesList_collection = bpy.props.CollectionProperty(type=INTERFACE_Files)

def MAIN_delProps():
    
    del bpy.types.Scene.BSM_TemplatesFilesList
    