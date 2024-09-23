import bpy
from .templates import *

class ExtensionPanel(bpy.types.Panel):
    bl_label = "Extensions"
    bl_idname = "OBJECT_PT_Extensions"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Script Manager"
    bl_order = 0
    
    template_index: bpy.props.IntProperty()
    
    def draw(self, context):
        layout = self.layout
        
        self.template_index = context.scene.templates_collection.find(context.scene.Templates)
        
        DRAW_Extensions(context, layout, self.template_index)

class TemplatesPanel(bpy.types.Panel):
    bl_label = "Templates"
    bl_idname = "OBJECT_PT_Templates"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Script Manager"
    bl_order = 1

    def draw(self, context):
        layout = self.layout
        
        ### --- GET PREFERENCES --- ###
        ###############################
        
        CHECKOUT_Preferences(layout)
        
        ### --- SETUP TEMPLATES --- ###
        ###############################
        
        SETUP_Templates(context, layout)

class ScriptsPanel(bpy.types.Panel):
    bl_label = "Scripts"
    bl_idname = "OBJECT_PT_Scripts"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Script Manager"
    bl_order = 2
    
    template_index: bpy.props.IntProperty()
    script_index: bpy.props.IntProperty()

    def draw(self, context):
        
        self.template_index = context.scene.templates_collection.find(context.scene.Templates)
        
        layout = self.layout
        
        if len(context.scene.templates_collection) != 0:
            if len(context.scene.templates_collection[self.template_index].scripts) != 0:
                for script in context.scene.templates_collection[self.template_index].scripts:
                    
                    box = layout.box()
                    
                    ### --- SUBPANEL --- ###
                    
                    panel_row = box.row()
                    icon = 'TRIA_DOWN' if script.status else 'TRIA_RIGHT'
                    panel_row.prop(script, "status", icon=icon, icon_only=True)
                    
                    ########################
                    
                    self.script_index = context.scene.templates_collection[self.template_index].scripts.find(script.name)
                    
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
            


MainClasses = [
    ExtensionPanel,
    TemplatesPanel,
    ScriptsPanel
]

def MainProps():
    pass
    

def delMainProps():
    pass
