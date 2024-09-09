import bpy


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

        new_name = "New Template"

        if len(context.scene.templates_collection) > 0:
            new_name = context.scene.templates_collection[-1].name + " 1"
        
        template = context.scene.templates_collection.add()

        template.name = new_name

        context.scene.Templates = template.name

        return {'FINISHED'}
    
class RemoveTemplateOperator(bpy.types.Operator):
    bl_idname = "templates.remove_item"
    bl_label = "Remove Item"
    
    index: bpy.props.IntProperty()
    
    def execute(self, context):
        
        if len(context.scene.templates_collection) > 0:
            context.scene.templates_collection.remove(self.index)
            
        if len(context.scene.templates_collection) > 0:
            bpy.context.scene.Templates = bpy.context.scene.templates_collection[0].name

        return {'FINISHED'}
    
class AddScriptOperator(bpy.types.Operator):
    bl_idname = "scripts.add_item"
    bl_label = "Add Item"

    template_index: bpy.props.IntProperty()

    name: bpy.props.StringProperty()

    def execute(self, context):
        
        template = context.scene.templates_collection[self.template_index]
        scripts = template.scripts.add()

        scripts.name = "Test"
        scripts.description = "Add Cube"
        scripts.icon = "PREFERENCE"
        scripts.path = "Test.py"

        return {'FINISHED'}
    
class RemoveScriptOperator(bpy.types.Operator):
    bl_idname = "scripts.remove_item"
    bl_label = "Remove Item"
    
    template_index: bpy.props.IntProperty()
    script_index: bpy.props.IntProperty()
    
    def execute(self, context):
        
        if len(context.scene.templates_collection[self.template_index].scripts) > 0:
            context.scene.templates_collection[self.template_index].scripts.remove(self.script_index)

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