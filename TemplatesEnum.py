import bpy
from .defers import addTemplate, removeTemplate, addScript, removeScript


class Scripts(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty()
    description: bpy.props.StringProperty()
    icon: bpy.props.StringProperty()
    path: bpy.props.StringProperty()

class TemplateName(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty()
    scripts: bpy.props.CollectionProperty(type=Scripts)

def get_template_items(self, context):
    
    Enum_items = []
    
    for template_item in context.scene.templates_collection:
        
        data = str(template_item.name)
        item = (data, data, data)
        
        Enum_items.append(item)
        
    return Enum_items

class AddTemplateOperator(bpy.types.Operator):
    bl_idname = "templates.add_item"
    bl_label = "Add Item"
    
    def execute(self, context):

        addTemplate(context)

        return {'FINISHED'}
    
class RemoveTemplateOperator(bpy.types.Operator):
    bl_idname = "templates.remove_item"
    bl_label = "Remove Item"
    
    index: bpy.props.IntProperty()
    
    def execute(self, context):
        
        removeTemplate(context, self.index)

        return {'FINISHED'}
    
class AddScriptOperator(bpy.types.Operator):
    bl_idname = "scripts.add_item"
    bl_label = "Add Item"

    template_index: bpy.props.IntProperty()

    name: bpy.props.StringProperty()

    def execute(self, context):
        
        addScript(context, self.template_index)

        return {'FINISHED'}
    
class RemoveScriptOperator(bpy.types.Operator):
    bl_idname = "scripts.remove_item"
    bl_label = "Remove Item"
    
    template_index: bpy.props.IntProperty()
    script_index: bpy.props.IntProperty()
    
    def execute(self, context):
        
        removeScript(context, self.template_index, self.script_index)

        return {'FINISHED'}

TemplateClasses = [
    Scripts,
    TemplateName,
    AddTemplateOperator,
    RemoveTemplateOperator,
    AddScriptOperator,
    RemoveScriptOperator
]

def TemplateProps():
    bpy.types.Scene.Templates = bpy.props.EnumProperty(items=get_template_items)
    bpy.types.Scene.templates_collection = bpy.props.CollectionProperty(type=TemplateName)

def delTemplateProps():

    del bpy.types.Scene.Templates
    del bpy.types.Scene.templates_collection