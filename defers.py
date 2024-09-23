import bpy, json, os, sys, importlib, inspect
from .interfaces import var_types, var_default_value

### GLOBALS Variables Control

def getVarType(types, id_type):
    value = ""
    index = 0
    # I need to find only whole name, ignore substrings
    str1 = " " + id_type + " "
    
    for vt in types:
        str2 = " " + vt[0] + " "
        if str1 in str2:
            value = vt[2]
            break
        index = index + 1
    return [value, index]

### JSON Data Control

def serializeDict(data):

    result = {
        "templates": []
    }

    for el in data:

        scripts_data = []

        if len(el.scripts) > 0:
            for script in el["scripts"]:
                
                arg_data = []
                
                for arg in script['args']:
                    
                    key = getVarType(var_types, arg['type'])[0]
                    
                    value = arg[key]      
                    
                    arg_data.append({
                        "name": arg['name'],
                        "description": arg['description'],
                        "type": arg['type'],
                        "value": value
                    })
                
                scripts_data.append({
                    "name": script["name"],
                    "description": script["description"],
                    "icon": script["icon"],
                    "path": script["path"],
                    "status": script['status'],
                    "args": arg_data
                })

        extensions_data = []
        
        if len(el.extensions) > 0:
            for extensions in el["extensions"]:
                
                extensions_data.append({
                    "name": extensions["name"],
                })
            


        result['templates'].append({
            "name": el["name"],
            "scripts": scripts_data,
            "extensions": extensions_data
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

### Extensions Control

def addExtension(context, template_index, name):
    template = context.scene.templates_collection[template_index]
    extension = template.extensions.add()
    
    extension.name = name

def removeExtension(context, template_index, extensions_index):
    if len(context.scene.templates_collection[template_index].extensions) > 0:
        context.scene.templates_collection[template_index].extensions.remove(extensions_index)
    
### Templates Control

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

### Scripts Control

def addScript(context, template_index, name = "Test", description = "Test Do", icon = "PREFERENCES", path = "Test.py", status=False):
    template = context.scene.templates_collection[template_index]
    script = template.scripts.add()

    script.name = name
    script.description = description
    script.icon = icon
    script.path = path
    script.status = status

def removeScript(context, template_index, script_index):

    if len(context.scene.templates_collection[template_index].scripts) > 0:
        context.scene.templates_collection[template_index].scripts.remove(script_index)
 
def editScript(context, template_index, script_index, name = "Test", description = "Test Do", icon = "PREFERENCES", path = "Test.py"):
    template = context.scene.templates_collection[template_index]
    script = template.scripts[script_index]

    script.name = name
    script.description = description
    script.icon = icon
    script.path = path
       
def getListOfScripts(self, context):
    """Get all scripts from preferences script directory folder"""
    preferences = bpy.context.preferences.addons["BlenderScriptManager"].preferences

    directory = preferences.script_dir
    
    Enum_items = []
    
    for filename in os.listdir(directory):
        # Check if the file ends with .py (Python files)
            if filename.endswith(".py"):
                data = filename
                item = (data, data, data)
                # Print the file name
                Enum_items.append(item)
        
    return Enum_items
    
### Arguments Control
    
def addArgs(context, template_index, script_index, type, name = "Test Arg", description = "Test Arg Do", value=0):
    template = context.scene.templates_collection[template_index]
    script = template.scripts[script_index]
    args = script.args
    
    arg = args.add()
    
    arg.name = name
    arg.description = description
    arg.type = type
    
    varType = getVarType(var_types, type)
    key = varType[0]
    index = varType[1]
    
    if value == 0 or value == "0":
        value = var_default_value[index]
    
    arg[key] = value
    
def editArgs(context, template_index, script_index, arg_index, type, name = "Test Arg", description = "Test Arg Do", value=0):
    template = context.scene.templates_collection[template_index]
    script = template.scripts[script_index]
    arg = script.args[arg_index]
    
    arg.name = name
    arg.description = description
    arg.type = type
    
    key = getVarType(var_types, type)[0]
        
    arg[key] = value[key]
    
def removeArgs(context, template_index, script_index, arg_index):
    template = context.scene.templates_collection[template_index]
    script = template.scripts[script_index]
    script.args.remove(arg_index)

### Scrirt Execution

def executeScript(props, filepath):
    # Dynamically import and execute the script
    spec = importlib.util.spec_from_file_location("module.name", filepath)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # Init Props value for script
    args = {}
    for prop in props:
        # Basic Properties or Cusom Object Properties
        key = getVarType(var_types, prop.type)[0]
        
        value = prop[key]
        
        prop_name = prop.name
        
        if "CUSTOM" in prop.type:
            sub_args = {}
            
            if prop.type == "CUSTOM":
                target_object = bpy.context.scene.objects.get(value)
            if prop.type == "CUSTOM_SELF":
                target_object = bpy.context.active_object
                
            for prop_item in target_object.keys():
                ignore_mask = prop_item + ";"
                if ignore_mask not in prop.name:
                    if prop_item != "_RNA_UI":
                        sub_args.update({prop_item: target_object[prop_item]})
            
            value = sub_args
            prop_name = target_object.name
            
        
        args.update({prop_name: value})
        
    # Assuming there's a function named 'main' in each script
    if hasattr(module, "main"):
        try:                
            module.main(args)  # Execute the 'main' function
            return [{'INFO'}, "Scripts executed"]
        except Exception as e:
            return [{'ERROR'}, f"Error running main() in {filepath}: {e}"]
        
def registerClass(filepath, fileName, isUnregister=False):
    # Full path to the .py file
    py_file_path = os.path.join(filepath, fileName)
    # Ensure the path is in Python's system path
    if filepath not in sys.path:
        sys.path.append(filepath)
        
    # Remove the .py extension from the filename to import the module
    module_name = os.path.splitext(fileName)[0]
    
    # Try to import the module dynamically
    try:
        module = importlib.import_module(module_name)
        importlib.reload(module)  # Reload the module in case it was already loaded
    except ImportError as e:
        print(f"Error importing module: {e}")
        module = None
        
    # If the module was successfully imported, inspect it to find all classes
    classes = []
    if module:
        # Iterate through the members of the module and filter out classes
        for name, obj in inspect.getmembers(module):
            # Check if the object is a class and a subclass of bpy.types.Operator or bpy.types.Panel
            if inspect.isclass(obj) and (issubclass(obj, bpy.types.Operator) or issubclass(obj, bpy.types.Panel)):
                classes.append(obj)

    if isUnregister:
        for cls in classes:
            # Check if the class exists in bpy.types (where all Blender classes are registered)
            _cls = getattr(bpy.types, cls.bl_idname, None)
            
            # If the class exists, try to unregister it
            if _cls:
                try:
                    bpy.utils.unregister_class(_cls)
                except RuntimeError as e:
                    print(f"Error unregistering class {cls.bl_idname}: {e}")
            else:
                print(f"Class {cls.bl_idname} not found in bpy.types")
    else:
        for cls in classes:
            bpy.utils.register_class(cls)
    