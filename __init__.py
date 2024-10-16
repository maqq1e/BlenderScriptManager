import bpy

from .App.Interfaces import INTERFACES_Classes
from .App.Operators import OPERATORS_Classes

from .Components.ExtensionsComponent import EXTENSIONS_Classes, EXTENSIONS_Props, EXTENSIONS_delProps
from .Components.TemplatesComponent import TEMPLATES_Classes, TEMPLATES_Props, TEMPLATES_delProps
from .main import MAIN_Classes, MAIN_Props, MAIN_delProps

from .Defers.Control import EXT_clearProperties

# Set information about addon
# Addon Info
bl_info = {
    "name": "Custom Script Manager",
    "author": "https://github.com/maqq1e/BlenderScriptManager",
    "description": "Easy way manage your custom scripts",
    "blender": (4, 2, 0),
    "version": (1, 0, 0),
}

# Preferences Panel

class SETTING_ManagerPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__
    
    script_dir: bpy.props.StringProperty(
        name="Scripts Directory",
        description="Select the directory containing the Python scripts",
        default="",
        subtype='DIR_PATH',
        update=EXT_clearProperties
    ) # type: ignore
    
    links_hide: bpy.props.BoolProperty(default=False)
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "script_dir")
        row = layout.row()
        if self.links_hide:
            row.prop(self, "links_hide", text="Links:", icon="TRIA_DOWN", toggle=True)
        else:
            row.prop(self, "links_hide", text="Links:", icon="TRIA_LEFT", toggle=True)
            
        if self.links_hide:
            op = layout.operator('wm.url_open', text="Project Git", icon="URL")
            op.url = "https://github.com/maqq1e/BlenderScriptManager"        
            row = layout.row()
            op = row.operator('wm.url_open', text="Github", icon="URL")
            op.url = "https://github.com/maqq1e"
            op = row.operator('wm.url_open', text="Gumroad", icon="URL")
            op.url = "https://maqq1e.gumroad.com/"
            op = row.operator('wm.url_open', text="ArtStation", icon="URL")
            op.url = "https://www.artstation.com/jellystuff"


# Initialization Classes
UsesClasses = []

UsesClasses.append(SETTING_ManagerPreferences)
UsesClasses.extend(INTERFACES_Classes)
UsesClasses.extend(OPERATORS_Classes)
UsesClasses.extend(EXTENSIONS_Classes)
UsesClasses.extend(TEMPLATES_Classes)
UsesClasses.extend(MAIN_Classes)

# Initialization Properties
def Props():
    MAIN_Props()
    EXTENSIONS_Props()
    TEMPLATES_Props()
def delProps():
    MAIN_delProps()
    EXTENSIONS_delProps()
    TEMPLATES_delProps()

# After Load
@bpy.app.handlers.persistent
def after_load(scene):
    EXT_clearProperties(scene, bpy.context)

# Handler for Event
event_handler = object()

# Register Classes
def register():

    for useClass in UsesClasses:
        bpy.utils.register_class(useClass)
    
    Props()
    
    # Triggers when window's workspace is changed
    subscribe_to = bpy.types.Window, "workspace"

    def change_template(context):
        if bpy.context.workspace.BSM_Templates == "":
            return None
        bpy.context.workspace.BSM_Templates = bpy.context.workspace.BSM_Templates # Active update event for property 
    bpy.msgbus.subscribe_rna(
        key=subscribe_to,
        owner=event_handler,
        args=(bpy.context,),
        notify=change_template,
    )
    bpy.msgbus.publish_rna(key=subscribe_to)
    
    bpy.app.handlers.load_post.append(after_load)


def unregister():
    for useClass in UsesClasses:
        bpy.utils.unregister_class(useClass)

    delProps()
    
    bpy.msgbus.clear_by_owner(event_handler)
    
    bpy.app.handlers.load_post.remove(after_load)

if __name__ == "__main__":
    register()
    
    
    