import bpy, json, os

def jsonImport(path, file_name):
    # set output path and file name (set your own)
    save_path = path
    file_name = os.path.join(save_path, file_name)

    # 2 - Import data from JSON file
    variable = {}

    # read JSON file
    with open(file_name, 'r') as f:
        variable = json.load(f)

    return variable


def generateTemplatesList():
    # Get the file name from the addon preferences
    preferences = bpy.context.preferences.addons["BlenderScriptManager"].preferences

    script_dir = preferences.script_dir

    items = []
    templates_list = jsonImport(script_dir, "templates.json")
    templates_list = templates_list['templates']

    for template in templates_list:
        items.append((template["name"], template["name"], template["name"]))

    return items
