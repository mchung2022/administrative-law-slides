import os
import json
import re

print("=== Fixing podcast_player.html with JSON.parse embedded script data ===")

json_synced_path = os.path.join(os.path.dirname(__file__), 'exact_synced_chapters.json')
script_json_path = os.path.join(os.path.dirname(__file__), 'podcast_script_30min.json')
html_path = os.path.join(os.path.dirname(__file__), '..', 'podcast_player.html')

with open(json_synced_path, 'r', encoding='utf8') as f:
    synced_chapters = json.load(f)

with open(script_json_path, 'r', encoding='utf8') as f:
    script_data = json.load(f)

script_dict = {}
for item in script_data:
    script_dict[str(item['id'])] = item['script']

js_chapters_json = json.dumps(synced_chapters, ensure_ascii=False)
js_script_json = json.dumps(script_dict, ensure_ascii=False)

with open(html_path, 'r', encoding='utf8') as f:
    html_content = f.read()

# Replace chapters
html_content = re.sub(
    r'const chapters = \[[\s\S]*?\];',
    lambda m: f'const chapters = {js_chapters_json};',
    html_content
)

# Replace fullScriptData dictionary with JSON.parse(...)
html_content = re.sub(
    r'const fullScriptData = (?:JSON\.parse\(.*?\)|{[\s\S]*?});',
    lambda m: f'const fullScriptData = JSON.parse({json.dumps(js_script_json)});',
    html_content
)

with open(html_path, 'w', encoding='utf8') as f:
    f.write(html_content)

print("[OK] Fixed JS script in podcast_player.html with JSON.parse!")
