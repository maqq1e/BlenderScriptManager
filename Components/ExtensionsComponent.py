import bpy

from ..interfaces import Extensions
from ..defers import getListOfScripts, addGlobalExtension, removeGlobalExtension

class AddExtensionsOperator(bpy.types.Operator):
    bl_idname = "extensions.add_item"
    bl_label = "Add Extension"

    name: bpy.props.EnumProperty(name="Scripts", items=getListOfScripts)

    def execute(self, context):

        addGlobalExtension(context, self.name)

        context.scene.BSM_isSave = True

        return {'FINISHED'}
    
    def invoke(self, context, event):

        return context.window_manager.invoke_props_dialog(self)

class RemoveExtensionsOperator(bpy.types.Operator):
    bl_idname = "extensions.remove_item"
    bl_label = "Remove Extension?"

    template_index: bpy.props.IntProperty()
    extension_index: bpy.props.IntProperty()

    def execute(self, context):

        removeGlobalExtension(context, self.extension_index)

        context.scene.BSM_isSave = True

        return {'FINISHED'}
    
    def invoke(self, context, event):

        return context.window_manager.invoke_confirm(self, event)

ExtensionsClasses = [
    AddExtensionsOperator,
    RemoveExtensionsOperator
]

def ExtensionsProps():
    bpy.types.Scene.BSM_Extensions_collection = bpy.props.CollectionProperty(type=Extensions)

def delExtensionsProps():    
    del bpy.types.Scene.BSM_Extensions_collection
    
def clearExtensionsProps():
    bpy.context.scene.BSM_Extensions_collection.clear()