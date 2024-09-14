import bpy
from .defers import addTemplate, removeTemplate, addScript, removeScript, editScript, addArgs, editArgs, getListOfScripts
from .GLOBAL import icons, var_types

class Args(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty()
    description: bpy.props.StringProperty()
    type: bpy.props.StringProperty()
    default: bpy.props.StringProperty()

class Scripts(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty()
    description: bpy.props.StringProperty()
    icon: bpy.props.StringProperty()
    path: bpy.props.StringProperty()
    status: bpy.props.BoolProperty()
    args: bpy.props.CollectionProperty(type=Args)

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

        context.scene.isSave = True

        return {'FINISHED'}
    
class RemoveTemplateOperator(bpy.types.Operator):
    bl_idname = "templates.remove_item"
    bl_label = "Remove Item"
    
    index: bpy.props.IntProperty()
    
    def execute(self, context):
        
        removeTemplate(context, self.index)

        context.scene.isSave = True

        return {'FINISHED'}
    
class AddScriptOperator(bpy.types.Operator):
    bl_idname = "scripts.add_item"
    bl_label = "Add Item"

    template_index: bpy.props.IntProperty(options={'HIDDEN'})

    name: bpy.props.StringProperty(name="Button Name")

    description: bpy.props.StringProperty(name="Description")

    icon: bpy.props.EnumProperty(name="Icons", items=icons)

    path: bpy.props.EnumProperty(name="Scripts", items=getListOfScripts)

    def execute(self, context):
        
        addScript(context, self.template_index, self.name, self.description, self.icon, self.path)

        context.scene.isSave = True

        return {'FINISHED'}
    
    def invoke(self, context, event):

        return context.window_manager.invoke_props_dialog(self)
    
class RemoveScriptOperator(bpy.types.Operator):
    bl_idname = "scripts.remove_item"
    bl_label = "Remove Item"
    
    template_index: bpy.props.IntProperty()
    script_index: bpy.props.IntProperty()
    
    def execute(self, context):
        
        removeScript(context, self.template_index, self.script_index)
        
        context.scene.isSave = True

        return {'FINISHED'}
    
class EditScriptOperator(bpy.types.Operator):
    bl_idname = "scripts.edit_item"
    bl_label = "Remove Item"
    
    template_index: bpy.props.IntProperty(options={'HIDDEN'})
    script_index: bpy.props.IntProperty(options={'HIDDEN'})

    name: bpy.props.StringProperty(name="Button Name")

    description: bpy.props.StringProperty(name="Description")

    icon: bpy.props.EnumProperty(name="Icons", items=icons)

    path: bpy.props.EnumProperty(name="Scripts", items=getListOfScripts)
    
    def execute(self, context):
        
        editScript(context, self.template_index, self.script_index, self.name, self.description, self.icon, self.path)
        
        context.scene.isSave = True

        return {'FINISHED'}
    
    def invoke(self, context, event):

        return context.window_manager.invoke_props_dialog(self)

class AddArgsOperator(bpy.types.Operator):
    bl_idname = "args.add_item"
    bl_label = "Add Arg Item"

    template_index: bpy.props.IntProperty(options={'HIDDEN'})
    script_index: bpy.props.IntProperty(options={'HIDDEN'})

    name: bpy.props.StringProperty(name="Args Name")

    description: bpy.props.StringProperty(name="Args Description")

    type: bpy.props.EnumProperty(name="Type", items=var_types)

    default: bpy.props.StringProperty(name="Args Default Value")

    def execute(self, context):
        
        addArgs(context, self.template_index, self.script_index, self.type, self.name, self.description, self.default)

        context.scene.isSave = True

        return {'FINISHED'}
    
    def invoke(self, context, event):

        return context.window_manager.invoke_props_dialog(self)

class EditArgsOperator(bpy.types.Operator):
    bl_idname = "args.edit_item"
    bl_label = "Remove Arg Item"
    
    template_index: bpy.props.IntProperty(options={'HIDDEN'})
    script_index: bpy.props.IntProperty(options={'HIDDEN'})
    arg_index: bpy.props.IntProperty(options={'HIDDEN'})

    name: bpy.props.StringProperty(name="Button Name")

    description: bpy.props.StringProperty(name="Description")

    type: bpy.props.EnumProperty(name="Type", items=var_types)

    default: bpy.props.StringProperty(name="Args Default Value")
    
    def execute(self, context):
        
        editArgs(context, self.template_index, self.script_index, self.arg_index, self.type, self.name, self.description, self.default)
        
        context.scene.isSave = True

        return {'FINISHED'}
    
    def invoke(self, context, event):

        return context.window_manager.invoke_props_dialog(self)
    
    
TemplateClasses = [
    Scripts,
    TemplateName,
    AddTemplateOperator,
    RemoveTemplateOperator,
    AddScriptOperator,
    RemoveScriptOperator,
    EditScriptOperator,
    AddArgsOperator,
    EditArgsOperator
]

def TemplateProps():
    bpy.types.Scene.Templates = bpy.props.EnumProperty(items=get_template_items)
    bpy.types.Scene.templates_collection = bpy.props.CollectionProperty(type=TemplateName)

    bpy.types.Scene.isSave = bpy.props.BoolProperty(default=False)

def delTemplateProps():

    del bpy.types.Scene.Templates
    del bpy.types.Scene.templates_collection