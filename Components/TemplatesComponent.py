import bpy
from ..defers import editTemplate, registerTemplateExtensions, addTemplate, removeTemplate, addScript, removeScript, editScript, addArgs, editArgs, removeArgs, getListOfScripts, registerClass, addGlobalExtension
from ..interfaces import *

def get_template_items(self, context):
    
    Enum_items = []
    
    for template_item in context.scene.BSM_Templates_collection:
        
        data = str(template_item.name)
        item = (data, data, data)
        
        Enum_items.append(item)
        
    return Enum_items   

def change_template_extensions(self, context):
    registerTemplateExtensions(context, self.BSM_Templates)

class AddTemplateOperator(bpy.types.Operator):
    bl_idname = "templates.add_item"
    bl_label = "Add Template"

    def execute(self, context):

        addTemplate(context)

        context.scene.BSM_isSave = True

        return {'FINISHED'}
   
class RemoveTemplateOperator(bpy.types.Operator):
    bl_idname = "templates.remove_item"
    bl_label = "Remove Template?"
    
    index: bpy.props.IntProperty()
    
    def execute(self, context):
        
        removeTemplate(context, self.index)

        context.scene.BSM_isSave = True

        return {'FINISHED'}
    
    def invoke(self, context, event):

        return context.window_manager.invoke_confirm(self, event)

class EditTemplateOperator(bpy.types.Operator):
    bl_idname = "templates.edit_item"
    bl_label = "Edit Template"
    
    template_index: bpy.props.IntProperty(options={'HIDDEN'})

    old_name: bpy.props.StringProperty(name="Old Name")
    
    name: bpy.props.StringProperty(name="New Name")
    
    def execute(self, context):
        
        editTemplate(context, self.template_index, self.name)
        
        context.scene.BSM_isSave = True

        return {'FINISHED'}
    
    def draw(self, context):
        layout = self.layout
        
        disbox = layout.box()
        disbox.prop(self, "old_name", text="Old Name")
        disbox.enabled = False
        
        box = layout.box()        
        box.prop(self, "name", text="New name")   
        
    
    def invoke(self, context, event):

        return context.window_manager.invoke_props_dialog(self)
 
class AddScriptOperator(bpy.types.Operator):
    bl_idname = "scripts.add_item"
    bl_label = "Add Script"

    template_index: bpy.props.IntProperty(options={'HIDDEN'})

    name: bpy.props.StringProperty(name="Button Name")

    description: bpy.props.StringProperty(name="Description")

    icon: bpy.props.EnumProperty(name="Icons", items=icons)

    path: bpy.props.EnumProperty(name="Scripts", items=getListOfScripts)

    def execute(self, context):
        
        addScript(context, self.template_index, self.name, self.description, self.icon, self.path)

        context.scene.BSM_isSave = True

        return {'FINISHED'}
    
    def invoke(self, context, event):

        return context.window_manager.invoke_props_dialog(self)
    
class RemoveScriptOperator(bpy.types.Operator):
    bl_idname = "scripts.remove_item"
    bl_label = "Remove Script from Template?"
    
    template_index: bpy.props.IntProperty()
    script_index: bpy.props.IntProperty()
    
    def execute(self, context):
        
        removeScript(context, self.template_index, self.script_index)
        
        context.scene.BSM_isSave = True

        return {'FINISHED'}
    
    def invoke(self, context, event):

        return context.window_manager.invoke_confirm(self, event)
    
class EditScriptOperator(bpy.types.Operator):
    bl_idname = "scripts.edit_item"
    bl_label = "Edit Script"
    
    template_index: bpy.props.IntProperty(options={'HIDDEN'})
    script_index: bpy.props.IntProperty(options={'HIDDEN'})

    name: bpy.props.StringProperty(name="Button Name")

    description: bpy.props.StringProperty(name="Description")

    icon: bpy.props.EnumProperty(name="Icons", items=icons)

    path: bpy.props.EnumProperty(name="Scripts", items=getListOfScripts)
    
    def execute(self, context):
        
        editScript(context, self.template_index, self.script_index, self.name, self.description, self.icon, self.path)
        
        context.scene.BSM_isSave = True

        return {'FINISHED'}
    
    def invoke(self, context, event):

        return context.window_manager.invoke_props_dialog(self)

class AddArgsOperator(bpy.types.Operator):
    bl_idname = "args.add_item"
    bl_label = "Add Arg Item"

    template_index: bpy.props.IntProperty(options={'HIDDEN'})
    script_index: bpy.props.IntProperty(options={'HIDDEN'})

    name: bpy.props.StringProperty(name="Name")

    description: bpy.props.StringProperty(name="Args Description")

    type: bpy.props.EnumProperty(name="Type", items=var_types)
    
    value: bpy.props.StringProperty(name="Object Name", default="0")

    def execute(self, context):
        if self.type == "CUSTOM":
            self.value = bpy.context.scene.BSM_activeObject.name
        if self.type == "CUSTOM_SELF":
            self.value = ""
        
        addArgs(context, self.template_index, self.script_index, self.type, self.name, self.description, self.value)

        context.scene.BSM_isSave = True

        return {'FINISHED'}
    
    def draw(self, context):
        
        layout = self.layout
        box = layout.box()
        
        if "CUSTOM" in self.type:
            box.prop(self, "name", text="Ignore Properties", placeholder="Prop1;Prop2;Prop3;")
        else:
            box.prop(self, "name", text="Name")
        box.prop(self, "description", text="Description")
        box.prop(self, "type", text="Type")
        
        if self.type == "CUSTOM":
            box.prop(context.scene, "BSM_activeObject", text="Object")
            
    
    def invoke(self, context, event):

        return context.window_manager.invoke_props_dialog(self)

class EditArgsOperator(bpy.types.Operator):
    bl_idname = "args.edit_item"
    bl_label = "Edit Arg Item"
    
    template_index: bpy.props.IntProperty(options={'HIDDEN'})
    script_index: bpy.props.IntProperty(options={'HIDDEN'})
    arg_index: bpy.props.IntProperty(options={'HIDDEN'})

    name: bpy.props.StringProperty(name="Name")

    description: bpy.props.StringProperty(name="Description")

    type: bpy.props.EnumProperty(name="Type", items=var_types)
    
    value: bpy.props.CollectionProperty(type=Args, options={'HIDDEN'})
    
    def execute(self, context):
        if self.type == "CUSTOM":
            self.value[0].custom = bpy.context.scene.BSM_activeObject.name
        if self.type == "CUSTOM_SELF":
            self.value[0].custom = ""
        
        editArgs(context, self.template_index, self.script_index, self.arg_index, self.type, self.name, self.description, self.value[0])
        
        context.scene.BSM_isSave = True

        return {'FINISHED'}
    
    def draw(self, context):
        
        layout = self.layout
        box = layout.box()
        
        if "CUSTOM" in self.type:
            box.prop(self, "name", text="Ignore Properties", placeholder="Prop1;Prop2;Prop3;")
        else:
            box.prop(self, "name", text="Name")
        box.prop(self, "description", text="Description")
        disbox = layout.box()
        disbox.prop(self, "type", text="Type")
        disbox.enabled = False
        
        if self.type == "CUSTOM":
            box.prop(context.scene, "BSM_activeObject", text="Object")
    
    def invoke(self, context, event):

        return context.window_manager.invoke_props_dialog(self)
    
class RemoveArgsOperator(bpy.types.Operator):
    bl_idname = "args.remove_item"
    bl_label = "Remove Argument from Script?"
    
    template_index: bpy.props.IntProperty(options={'HIDDEN'})
    script_index: bpy.props.IntProperty(options={'HIDDEN'})
    arg_index: bpy.props.IntProperty(options={'HIDDEN'})
    
    def execute(self, context):
        
        removeArgs(context, self.template_index, self.script_index, self.arg_index)
        
        context.scene.BSM_isSave = True

        return {'FINISHED'}
    
    def invoke(self, context, event):

        return context.window_manager.invoke_confirm(self, event)
    
TemplateClasses = [
    AddTemplateOperator,
    RemoveTemplateOperator,
    EditTemplateOperator,
    AddScriptOperator,
    RemoveScriptOperator,
    EditScriptOperator,
    AddArgsOperator,
    EditArgsOperator,
    RemoveArgsOperator
]

def TemplateProps():
    bpy.types.WorkSpace.BSM_Templates = bpy.props.EnumProperty(items=get_template_items, update=change_template_extensions)
    
    bpy.types.Scene.BSM_Templates_collection = bpy.props.CollectionProperty(type=TemplateName)

    bpy.types.Scene.BSM_isSave = bpy.props.BoolProperty(default=False)
    
    bpy.types.Scene.BSM_activeObject = bpy.props.PointerProperty(type=bpy.types.Object)

def delTemplateProps():

    del bpy.types.WorkSpace.BSM_Templates
    del bpy.types.Scene.BSM_Templates_collection
    del bpy.types.Scene.BSM_isSave
    del bpy.types.Scene.BSM_activeObject
    
def clearTemplateProps():
    pass