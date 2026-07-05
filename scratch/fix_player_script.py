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
for ch in script_data:
    cid = str(ch['id'])
    full_text = "\n\n".join([f"【{l['speaker']}】：{l['text']}" for l in ch['lines']])
    script_dict[cid] = full_text

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

# Update duration display to 26:43
html_content = html_content.replace('id="durationTime">29:17</span>', 'id="durationTime">26:43</span>')
html_content = html_content.replace('id="durationTime">30:00</span>', 'id="durationTime">26:43</span>')

with open(html_path, 'w', encoding='utf8') as f:
    f.write(html_content)

print("[OK] Successfully updated podcast_player.html with Dual-Host Synced Timeline!")
