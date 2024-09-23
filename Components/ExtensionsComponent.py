import bpy

from ..interfaces import Extensions
from ..defers import getListOfScripts, addExtension, removeExtension

class AddExtensionsOperator(bpy.types.Operator):
    bl_idname = "extensions.add_item"
    bl_label = "Add Extension"
    
    template_index: bpy.props.IntProperty(options={'HIDDEN'})

    name: bpy.props.EnumProperty(name="Scripts", items=getListOfScripts)

    def execute(self, context):

        addExtension(context, self.template_index, self.name)

        context.scene.isSave = True

        return {'FINISHED'}
    
    def invoke(self, context, event):

        return context.window_manager.invoke_props_dialog(self)

class RemoveExtensionsOperator(bpy.types.Operator):
    bl_idname = "extensions.remove_item"
    bl_label = "Remove Extension?"

    template_index: bpy.props.IntProperty()
    extension_index: bpy.props.IntProperty()

    def execute(self, context):

        removeExtension(context, self.template_index, self.extension_index)

        context.scene.isSave = True

        return {'FINISHED'}
    
    def invoke(self, context, event):

        return context.window_manager.invoke_confirm(self, event)




ExtensionsClasses = [
    AddExtensionsOperator,
    RemoveExtensionsOperator
]

def ExtensionsProps():
    bpy.types.Scene.extensions_collection = bpy.props.CollectionProperty(type=Extensions)

def delExtensionsProps():

    del bpy.types.Scene.extensions_collection