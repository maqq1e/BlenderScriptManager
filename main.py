import bpy

       
class InfoTab(bpy.types.Panel):
    bl_label = "Script Manager"
    bl_idname = "OBJECT_PT_custom_scripts_manager"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Script Manager"        

    def draw(self, context):

        selected_obj = context.selected_objects

        layout = self.layout

        box = layout.box()
        box.label(text="Test")



UsesClasses = [
    InfoTab,
]

def UsesProps():

    bpy.types.Scene.Test = bpy.props.StringProperty(
        name="",
        default=""
    )

    
