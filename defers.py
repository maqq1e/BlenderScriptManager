import bpy, json, os

def serializeDict(data):

    result = {
        "templates": []
    }

    for el in data:

        scripts_data = []

        if len(el.scripts) > 0:
            for script in el["scripts"]:
                scripts_data.append({
                    "name": script["name"],
                    "description": script["description"],
                    "icon": script["icon"],
                    "path": script["path"],
                })

        result['templates'].append({
            "name": el["name"],
            "scripts": scripts_data
        })


    return result

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

def jsonExport(path, file_name, data):
    # encode dict as JSON 
    payload = json.dumps(data, indent=1, ensure_ascii=True)

    # set output path and file name (set your own)
    save_path = path
    file_name = os.path.join(save_path, file_name)

    # write JSON file
    with open(file_name, 'w') as outfile:
        outfile.write(payload + '\n')

def addTemplate(context, new_name = "New Template"):

    if new_name == "New Template":
        if len(context.scene.templates_collection) > 0:
            new_name = context.scene.templates_collection[-1].name + " 1"
        
    template = context.scene.templates_collection.add()

    template.name = new_name

    context.scene.Templates = template.name

def removeTemplate(context, index):
    if len(context.scene.templates_collection) > 0:
            context.scene.templates_collection.remove(index)
            
    if len(context.scene.templates_collection) > 0:
        bpy.context.scene.Templates = bpy.context.scene.templates_collection[0].name

def addScript(context, template_index, name = "Test", description = "Test Do", icon = "PREFERENCES", path = "Test.py"):
    template = context.scene.templates_collection[template_index]
    scripts = template.scripts.add()

    scripts.name = name
    scripts.description = description
    scripts.icon = icon
    scripts.path = path

def removeScript(context, template_index, script_index):
    if len(context.scene.templates_collection[template_index].scripts) > 0:
        context.scene.templates_collection[template_index].scripts.remove(script_index)