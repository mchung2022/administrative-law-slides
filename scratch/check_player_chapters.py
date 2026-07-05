import json
import re

with open('podcast_player.html', 'r', encoding='utf8') as f:
    html = f.read()

ch_match = re.search(r'const chapters = (\[[\s\S]*?\]);', html)
if ch_match:
    print("=== Chapters in podcast_player.html ===")
    ch_data = json.loads(ch_match.group(1))
    for c in ch_data:
        print(f"Chapter {c['id']:2d}: start={c['start']:7.2f}s ({c['time']}), end={c['end']:7.2f}s | Title: {c['title']}")

print("\n=== Checking fullScriptData keys in podcast_player.html ===")
fs_match = re.search(r'const fullScriptData = (JSON\.parse\(.*?\));', html)
if fs_match:
    raw_json_str = fs_match.group(1).replace('JSON.parse(', '')[:-1]
    inner_json = json.loads(raw_json_str)
    dict_data = json.loads(inner_json)
    print("fullScriptData keys:", sorted([int(k) for k in dict_data.keys()]))
    for k in sorted([int(k) for k in dict_data.keys()]):
        print(f"Key {k:2d}: length = {len(dict_data[str(k)])} chars")
