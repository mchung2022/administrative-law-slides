import os
import json
import re

print("=== Embedding Exact 30-Min Synced Chapter Array into podcast_player.html ===")

json_synced_path = os.path.join(os.path.dirname(__file__), 'exact_synced_chapters.json')
script_json_path = os.path.join(os.path.dirname(__file__), 'podcast_script_30min.json')
html_path = os.path.join(os.path.dirname(__file__), '..', 'podcast_player.html')

with open(json_synced_path, 'r', encoding='utf8') as f:
    synced_chapters = json.load(f)

with open(script_json_path, 'r', encoding='utf8') as f:
    script_data = json.load(f)

script_dict = {}
for item in script_data:
    script_dict[item['id']] = item['script']

# Format JS array for chapters
js_chapters_str = json.dumps(synced_chapters, ensure_ascii=False, indent=12)
js_script_dict_str = json.dumps(script_dict, ensure_ascii=False, indent=12)

with open(html_path, 'r', encoding='utf8') as f:
    html_content = f.read()

# Replace chapters definition
html_content = re.sub(
    r'const chapters = \[[\s\S]*?\];',
    f'const chapters = {js_chapters_str};',
    html_content
)

# Replace fullScriptData definition
html_content = re.sub(
    r'const fullScriptData = {[\s\S]*?};',
    f'const fullScriptData = {js_script_dict_str};',
    html_content
)

# Replace duration label default to 29:17
html_content = html_content.replace('id="durationTime">30:00</span>', 'id="durationTime">29:17</span>')
html_content = html_content.replace('max="1800"', 'max="1757"')
html_content = html_content.replace('|| 1800', '|| 1757')

with open(html_path, 'w', encoding='utf8') as f:
    f.write(html_content)

print(f"✅ Successfully updated {html_path} with 100% synchronized chapter timeline!")
