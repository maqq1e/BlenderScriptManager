import bpy
from .main import UsesClasses, UsesProps

addon_keymaps = []

# Addon Info
bl_info = {
    "name": "Custom Script Manager",
    "author": "daniel.hovach@gmail.com",
    "description": "Easy way manage your custom scripts",
    "blender": (4, 0, 0),
    "version": (0, 0, 1),
}

# Register Classes 
def register():
    UsesProps()

    for useClass in UsesClasses:
        bpy.utils.register_class(useClass)


def unregister():
    for useClass in UsesClasses:
        bpy.utils.unregister_class(useClass)


if __name__ == "__main__":
    register()
