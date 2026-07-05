import os
import json
import re
import asyncio
import edge_tts
from measure_mp3_duration import get_mp3_duration

print("=== Calibrating 30-Minute Exact Audio Synthesis (rate='-30%') ===")

json_path = os.path.join(os.path.dirname(__file__), 'podcast_script_30min.json')
output_dir = os.path.join(os.path.dirname(__file__), 'ch_audio_30min')
os.makedirs(output_dir, exist_ok=True)

final_mp3_path = os.path.join(os.path.dirname(__file__), '..', 'podcast_audio_30min.mp3')

with open(json_path, 'r', encoding='utf8') as f:
    chapters = json.load(f)

VOICE = "zh-TW-HsiaoChenNeural"

async def synthesize_chapter(ch):
    cid = ch['id']
    raw_text = ch['script']
    clean_text = re.sub(r'【.*?】', '', raw_text)
    clean_text = re.sub(r'（.*?）', '', clean_text).strip()
    
    ch_mp3 = os.path.join(output_dir, f"ch_{cid}.mp3")
    print(f"[Chapter {cid}/10] Synthesizing {len(clean_text)} chars with rate='-30%'...")
    
    for attempt in range(1, 4):
        try:
            comm = edge_tts.Communicate(clean_text, VOICE, rate="-30%")
            await comm.save(ch_mp3)
            dur = get_mp3_duration(ch_mp3)
            print(f"[OK] Chapter {cid} completed: {dur:.2f} seconds ({dur/60:.2f} mins).")
            return ch_mp3, dur
        except Exception as e:
            print(f"⚠️ Attempt {attempt} failed for Ch {cid}: {e}")
            await asyncio.sleep(2)
            
    raise Exception(f"Failed Ch {cid}")

async def main():
    results = []
    for ch in chapters:
        res = await synthesize_chapter(ch)
        results.append(res)
        await asyncio.sleep(1.2)

    ch_files = [r[0] for r in results]
    ch_durations = [r[1] for r in results]
    
    total_dur = sum(ch_durations)
    print(f"\nTotal 10 Chapters Raw Audio Duration: {total_dur:.2f} seconds ({total_dur/60:.2f} mins)")

    # Concatenate MP3 files
    with open(final_mp3_path, 'wb') as outfile:
        for fpath in ch_files:
            with open(fpath, 'rb') as infile:
                outfile.write(infile.read())
                
    final_dur = get_mp3_duration(final_mp3_path)
    size_mb = os.path.getsize(final_mp3_path) / (1024 * 1024)
    print(f"🎉 Final MP3 Created: {final_mp3_path}")
    print(f"🎉 Total Exact Duration: {final_dur:.2f} seconds ({final_dur/60:.2f} mins) | Size: {size_mb:.2f} MB")

if __name__ == '__main__':
    asyncio.run(main())
