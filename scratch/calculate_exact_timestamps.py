import os
import json
import re
import asyncio
import edge_tts
from measure_mp3_duration import get_mp3_duration

print("=== Generating Exact 30-Minute Broadcast MP3 (rate='-40%') & Sync Timestamps ===")

json_path = os.path.join(os.path.dirname(__file__), 'podcast_script_30min.json')
output_dir = os.path.join(os.path.dirname(__file__), 'ch_audio_exact30')
os.makedirs(output_dir, exist_ok=True)

final_mp3_path = os.path.join(os.path.dirname(__file__), '..', 'podcast_audio_30min.mp3')

with open(json_path, 'r', encoding='utf8') as f:
    chapters = json.load(f)

VOICE = "zh-TW-HsiaoChenNeural"  # Professional Radio Presenter Voice

def format_mmss(seconds):
    m = int(seconds // 60)
    s = int(seconds % 60)
    return f"{m:02d}:{s:02d}"

async def main():
    ch_files = []
    ch_durations = []
    
    for ch in chapters:
        cid = ch['id']
        raw_text = ch['script']
        clean_text = re.sub(r'【.*?】', '', raw_text)
        clean_text = re.sub(r'（.*?）', '', clean_text).strip()
        
        ch_mp3 = os.path.join(output_dir, f"ch_{cid}.mp3")
        print(f"[Chapter {cid}/10] Synthesizing {len(clean_text)} chars with rate='-40%'...")
        
        comm = edge_tts.Communicate(clean_text, VOICE, rate="-40%")
        await comm.save(ch_mp3)
        dur = get_mp3_duration(ch_mp3)
        print(f"[OK] Ch {cid} duration: {dur:.2f}s ({format_mmss(dur)})")
        ch_files.append(ch_mp3)
        ch_durations.append(dur)
        await asyncio.sleep(1.0)

    # Concatenate MP3 files
    with open(final_mp3_path, 'wb') as outfile:
        for fpath in ch_files:
            with open(fpath, 'rb') as infile:
                outfile.write(infile.read())
                
    total_sec = get_mp3_duration(final_mp3_path)
    size_mb = os.path.getsize(final_mp3_path) / (1024 * 1024)
    print(f"\n[OK] Combined Final MP3 Duration: {total_sec:.2f}s ({format_mmss(total_sec)}) | Size: {size_mb:.2f} MB")

    # Build exact synchronized chapters array for JS
    exact_chapters = []
    current_sec = 0.0
    for idx, ch in enumerate(chapters):
        dur = ch_durations[idx]
        start_sec = round(current_sec, 2)
        end_sec = round(current_sec + dur, 2)
        start_mmss = format_mmss(start_sec)
        
        exact_chapters.append({
            "id": ch['id'],
            "start": start_sec,
            "end": end_sec,
            "time": start_mmss,
            "title": ch['title'],
            "topic": ch['topic']
        })
        current_sec = end_sec

    synced_json_path = os.path.join(os.path.dirname(__file__), 'exact_synced_chapters.json')
    with open(synced_json_path, 'w', encoding='utf8') as f:
        json.dump(exact_chapters, f, ensure_ascii=False, indent=2)

    print(f"[OK] Saved Exact Synced Chapters JSON to {synced_json_path}")

if __name__ == '__main__':
    asyncio.run(main())
