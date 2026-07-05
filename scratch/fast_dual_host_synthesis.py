import os
import json
import re
import asyncio
import edge_tts
from measure_mp3_duration import get_mp3_duration

print("=== Fast Concurrent Dual-Host Speech Synthesis (YunJhe & HsiaoChen) ===")

json_path = os.path.join(os.path.dirname(__file__), 'podcast_script_30min.json')
output_dir = os.path.join(os.path.dirname(__file__), 'ch_audio_dual_fast')
os.makedirs(output_dir, exist_ok=True)

final_mp3_path = os.path.join(os.path.dirname(__file__), '..', 'podcast_audio_30min.mp3')

with open(json_path, 'r', encoding='utf8') as f:
    chapters = json.load(f)

def format_mmss(seconds):
    m = int(seconds // 60)
    s = int(seconds % 60)
    return f"{m:02d}:{s:02d}"

async def synthesize_line(clean_text, voice, line_mp3, semaphore):
    async with semaphore:
        comm = edge_tts.Communicate(clean_text, voice, rate="-40%")
        await comm.save(line_mp3)

async def synthesize_chapter(ch, semaphore):
    cid = ch['id']
    lines = ch['lines']
    ch_dir = os.path.join(output_dir, f"ch_{cid}")
    os.makedirs(ch_dir, exist_ok=True)
    
    line_tasks = []
    line_files = []
    for l_idx, line in enumerate(lines):
        voice = line['voice']
        text = line['text']
        clean_text = re.sub(r'【.*?】', '', text)
        clean_text = re.sub(r'（.*?）', '', clean_text).strip()
        
        line_mp3 = os.path.join(ch_dir, f"line_{l_idx+1}.mp3")
        line_files.append(line_mp3)
        line_tasks.append(synthesize_line(clean_text, voice, line_mp3, semaphore))
        
    await asyncio.gather(*line_tasks)
    
    # Concatenate chapter lines into ch_X.mp3
    ch_mp3 = os.path.join(output_dir, f"ch_{cid}.mp3")
    with open(ch_mp3, 'wb') as outfile:
        for fpath in line_files:
            with open(fpath, 'rb') as infile:
                outfile.write(infile.read())
                
    dur = get_mp3_duration(ch_mp3)
    print(f"[Chapter {cid}/10 OK] Duration: {dur:.2f}s ({format_mmss(dur)}) | {len(lines)} Dialogue Lines")
    return cid, ch_mp3, dur

async def main():
    semaphore = asyncio.Semaphore(5) # max 5 concurrent requests
    
    tasks = [synthesize_chapter(ch, semaphore) for ch in chapters]
    results = await asyncio.gather(*tasks)
    
    # Sort results by chapter ID
    results.sort(key=lambda x: x[0])
    
    ch_files = [r[1] for r in results]
    ch_durations = [r[2] for r in results]

    # Combine all 10 chapters into final_mp3_path
    with open(final_mp3_path, 'wb') as outfile:
        for fpath in ch_files:
            with open(fpath, 'rb') as infile:
                outfile.write(infile.read())
                
    total_sec = get_mp3_duration(final_mp3_path)
    size_mb = os.path.getsize(final_mp3_path) / (1024 * 1024)
    print(f"\n[OK] Final Dual-Host MP3 Duration: {total_sec:.2f}s ({format_mmss(total_sec)}) | Size: {size_mb:.2f} MB")

    # Generate exact timeline markers
    exact_chapters = []
    current_sec = 0.0
    for idx, ch in enumerate(chapters):
        dur = ch_durations[idx]
        start_sec = round(current_sec, 2)
        end_sec = round(current_sec + dur, 2)
        start_mmss = format_mmss(start_sec)
        
        full_text = "\n\n".join([f"【{l['speaker']}】：{l['text']}" for l in ch['lines']])
        
        exact_chapters.append({
            "id": ch['id'],
            "start": start_sec,
            "end": end_sec,
            "time": start_mmss,
            "title": ch['title'],
            "topic": ch['topic'],
            "script": full_text
        })
        current_sec = end_sec

    synced_json_path = os.path.join(os.path.dirname(__file__), 'exact_synced_chapters.json')
    with open(synced_json_path, 'w', encoding='utf8') as f:
        json.dump(exact_chapters, f, ensure_ascii=False, indent=2)

    print(f"[OK] Saved Dual-Host Synced Chapters JSON to {synced_json_path}")

if __name__ == '__main__':
    asyncio.run(main())
