import bpy
from enum import Enum

from ..App.Interfaces import INTERFACE_Extensions
from ..Defers.Control import *


class EXTENSIONS(Enum):
    extensions_add_item = "extensions.add_item"
    extensions_remove_item = "extensions.remove_item"

class EXTENSION_AddExtensionsOperator(bpy.types.Operator):
    bl_idname = EXTENSIONS.extensions_add_item.value
    bl_label = "Add Extension"

    name: bpy.props.EnumProperty(name="Scripts", items=getListOfScripts)

    def execute(self, context):

        CMP_addGlobalExtension(context, self.name)

        context.scene.BSM_isSave = True

        return {'FINISHED'}
    
    def invoke(self, context, event):

        return context.window_manager.invoke_props_dialog(self)

class EXTENSION_RemoveExtensionsOperator(bpy.types.Operator):
    bl_idname = EXTENSIONS.extensions_remove_item.value
    bl_label = "Remove Extension?"

    template_index: bpy.props.IntProperty()
    extension_index: bpy.props.IntProperty()

    def execute(self, context):

        CMP_removeGlobalExtension(context, self.extension_index)

        context.scene.BSM_isSave = True

        return {'FINISHED'}
    
    def invoke(self, context, event):

        return context.window_manager.invoke_confirm(self, event)

EXTENSIONS_Classes = [
    EXTENSION_AddExtensionsOperator,
    EXTENSION_RemoveExtensionsOperator
]

def EXTENSIONS_Props():
    bpy.types.Scene.BSM_Extensions_collection = bpy.props.CollectionProperty(type=INTERFACE_Extensions)

def EXTENSIONS_delProps():    
    del bpy.types.Scene.BSM_Extensions_collection