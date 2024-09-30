import bpy, os
from .main import MainClasses, MainProps, delMainProps

from .interfaces import InterfaceClasses
from .operators import OperatorsClasses
from .Components.TemplatesComponent import TemplateClasses, TemplateProps, delTemplateProps
from .Components.ExtensionsComponent import ExtensionsClasses, ExtensionsProps, delExtensionsProps

# Addon Info
bl_info = {
    "name": "Custom Script Manager",
    "author": "https://github.com/maqq1e",
    "description": "Easy way manage your custom scripts",
    "blender": (4, 2, 0),
    "version": (0, 8, 0),
}

# Preferences Panel 

class ManagerPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__
    
    script_dir: bpy.props.StringProperty(
        name="Scripts Directory",
        description="Select the directory containing the Python scripts",
        default="",
        subtype='DIR_PATH',
    ) # type: ignore
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "script_dir")


# Initialization Classes

UsesClasses = []

UsesClasses.append(ManagerPreferences)
UsesClasses.extend(InterfaceClasses)
UsesClasses.extend(OperatorsClasses)
UsesClasses.extend(ExtensionsClasses)
UsesClasses.extend(MainClasses)
UsesClasses.extend(TemplateClasses)

# Initialization Properties

def Props():
    
    MainProps()
    ExtensionsProps()
    TemplateProps()

def delProps():
    
    delMainProps()
    delExtensionsProps()
    delTemplateProps()


event_handler = object() # Handler for Event

# Register Classes 
def register():

    for useClass in UsesClasses:
        bpy.utils.register_class(useClass)
        
    Props()
    
    # Triggers when window's workspace is changed
    subscribe_to = bpy.types.Window, "workspace"

    def change_template(context):
        bpy.context.workspace.Templates = bpy.context.workspace.Templates # Active update event for property 
        
    bpy.msgbus.subscribe_rna(
        key=subscribe_to,
        owner=event_handler,
        args=(bpy.context,),
        notify=change_template,
    )

    bpy.msgbus.publish_rna(key=subscribe_to)


def unregister():
    for useClass in UsesClasses:
        bpy.utils.unregister_class(useClass)

    delProps()
    
    bpy.msgbus.clear_by_owner(event_handler)

if __name__ == "__main__":
    register()
