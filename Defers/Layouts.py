import bpy, textwrap

def LAYOUT_multiline(context, text, parent):
    chars = int(context.region.width / 7)   # 7 pix on 1 character
    wrapper = textwrap.TextWrapper(width=chars)
    text_lines = wrapper.wrap(text=text)
    for text_line in text_lines:
        parent.label(text=text_line)
        
def getPreferences():
    data = bpy.context.preferences.addons["bl_ext.user_default.custom_script_manager"].preferences
    return data
 