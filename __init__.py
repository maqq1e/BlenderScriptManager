import bpy
from .main import UsesClasses, MainProps, delMainProps

# Addon Info
bl_info = {
    "name": "Custom Script Manager",
    "author": "https://github.com/maqq1e",
    "description": "Easy way manage your custom scripts",
    "blender": (4, 0, 0),
    "version": (0, 1, 0),
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


UsesClasses.append(ManagerPreferences)

# Register Classes 
def register():

    for useClass in UsesClasses:
        bpy.utils.register_class(useClass)
    
    MainProps()


def unregister():
    for useClass in UsesClasses:
        bpy.utils.unregister_class(useClass)

    delMainProps()


if __name__ == "__main__":
    register()
