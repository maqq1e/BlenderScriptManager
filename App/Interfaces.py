import bpy, os

from ..Defers.Control import makeTemplateSave

### Classes

class INTERFACE_Args(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty()
    description: bpy.props.StringProperty()
    type: bpy.props.StringProperty()
    bool: bpy.props.BoolProperty(options={'ANIMATABLE'})
    bool_toggle: bpy.props.BoolProperty(options={'ANIMATABLE'})
    float: bpy.props.FloatProperty()
    float_slider: bpy.props.FloatProperty()
    string: bpy.props.StringProperty(
        name="Directory",
        default="",
        subtype='NONE'
    )
    integer: bpy.props.IntProperty()
    integer_slider: bpy.props.IntProperty()
    string_path: bpy.props.StringProperty(
        name="Directory",
        default="",
        subtype='DIR_PATH'
    )
    custom: bpy.props.StringProperty()
    custom_self: bpy.props.StringProperty()

class INTERFACE_Scripts(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty()
    description: bpy.props.StringProperty()
    icon: bpy.props.StringProperty()
    path: bpy.props.StringProperty()
    status: bpy.props.BoolProperty()
    args: bpy.props.CollectionProperty(type=INTERFACE_Args)

class INTERFACE_Extensions(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty()
    status: bpy.props.BoolProperty()
    
class INTERFACE_TemplateName(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(update=makeTemplateSave)
    scripts: bpy.props.CollectionProperty(type=INTERFACE_Scripts)
    extensions: bpy.props.CollectionProperty(type=INTERFACE_Extensions)

class INTERFACE_Files(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty()

INTERFACES_Classes = [
    INTERFACE_Args,
    INTERFACE_Scripts,
    INTERFACE_Extensions,
    INTERFACE_TemplateName,    
    INTERFACE_Files,
]