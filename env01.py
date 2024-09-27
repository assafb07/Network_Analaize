import sys
import re
from dotenv import load_dotenv, dotenv_values
import os

env_list = ["gemini_key", "main_theme", "enc_key", "font_size", "font", "default_font", "default_fsize", "default_top_size_position",
"top_size_position", "main_windows_font_size", "main_windows_font", "gemini_font", "default_gemini_font", "gemini_font_size",
"default_gemini_font_size", "gemini_size_position", "default_gemini_size_position", "response_time"]

def chenge_var(key_to_edit, new_var):
#    print(os.getenv(key_to_edit))
    try:
        dotenv = sys.argv[1]
    except IndexError as e:
        dotenv = '.env'

    with open(dotenv, 'r') as f:
        content = f.readlines()

    contentList = [x.strip().split('#')[0].split('=', 1) for x in content if '=' in x.split('#')[0]]
    contentDict = dict(contentList)
    for k, v in contentList:
        for i, x in enumerate(v.split('$')[1:]):
            key = re.findall(r'\w+', x)[0]
            v = v.replace('$' + key, contentDict[key])
        contentDict[k] = v
    contentDict[key_to_edit] = new_var

    with open(".env", "w") as file:
        file.write("")

    for k, v in contentDict.items():
        with open(".env", "a") as file:
            file.write("%s=%s\n" % (k, v))
        os.environ[k] = v

def delete_env():

    for item in env_list:
        os.unsetenv(item)
