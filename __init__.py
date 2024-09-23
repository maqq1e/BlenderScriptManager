import bpy
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
    "version": (0, 6, 5),
}

# Preferences Panel 
class ManagerPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__
    
    script_dir: bpy.props.StringProperty(
        name="Scripts Directory",
        description="Select the directory containing the Python scripts",
        default="C:\Program Files (x86)\Steam\steamapps\common\Blender\/4.2\_additional\Custom Scripts\/",
        subtype='DIR_PATH'
    ) # type: ignore

    templates_list: bpy.props.StringProperty(
        name="Scripts Directory",
        description="Select the directory containing the Python scripts",
        default="",
        subtype='DIR_PATH'
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
    TemplateProps()
    ExtensionsProps()

def delProps():
    
    delMainProps()
    delTemplateProps()
    delExtensionsProps()

# Register Classes 
def register():

    for useClass in UsesClasses:
        bpy.utils.register_class(useClass)
        
    Props()


def unregister():
    for useClass in UsesClasses:
        bpy.utils.unregister_class(useClass)

    delProps()


if __name__ == "__main__":
    register()
