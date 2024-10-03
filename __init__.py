import bpy
from .main import MainClasses, MainProps, delMainProps, clearMainProps

from .defers import clearProperties

from .interfaces import InterfaceClasses
from .operators import OperatorsClasses
from .Components.TemplatesComponent import TemplateClasses, TemplateProps, delTemplateProps, clearTemplateProps
from .Components.ExtensionsComponent import ExtensionsClasses, ExtensionsProps, delExtensionsProps, clearExtensionsProps

# Addon Info
bl_info = {
    "name": "Custom Script Manager",
    "author": "https://github.com/maqq1e",
    "description": "Easy way manage your custom scripts",
    "blender": (4, 2, 0),
    "version": (0, 9, 6),
}

# Preferences Panel

class ManagerPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__
    
    script_dir: bpy.props.StringProperty(
        name="Scripts Directory",
        description="Select the directory containing the Python scripts",
        default="",
        subtype='DIR_PATH',
        update=clearProperties
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
UsesClasses.extend(TemplateClasses)
UsesClasses.extend(MainClasses)

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
        bpy.context.workspace.BSM_Templates = bpy.context.workspace.BSM_Templates # Active update event for property 
        
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