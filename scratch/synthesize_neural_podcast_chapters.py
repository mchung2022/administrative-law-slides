import os
import json
import re
import asyncio
import edge_tts

print("=== Fast Chapter-by-Chapter Neural Broadcast Voice Synthesis (zh-TW-YunJheNeural) ===")

json_path = os.path.join(os.path.dirname(__file__), 'podcast_script_30min.json')
output_dir = os.path.join(os.path.dirname(__file__), 'ch_audio')
os.makedirs(output_dir, exist_ok=True)

final_mp3_path = os.path.join(os.path.dirname(__file__), '..', 'podcast_audio_30min.mp3')

with open(json_path, 'r', encoding='utf8') as f:
    chapters = json.load(f)

VOICE = "zh-TW-YunJheNeural"  # Professional Male Broadcast Host Voice

async def synthesize_chapter(ch):
    cid = ch['id']
    raw_text = ch['script']
    clean_text = re.sub(r'【.*?】', '', raw_text)
    clean_text = re.sub(r'（.*?）', '', clean_text).strip()
    
    ch_mp3 = os.path.join(output_dir, f"ch_{cid}.mp3")
    print(f"[Chapter {cid}/10] Synthesizing {len(clean_text)} chars -> {ch_mp3} ...")
    
    communicate = edge_tts.Communicate(clean_text, VOICE, rate="+0%", volume="+0%")
    await communicate.save(ch_mp3)
    print(f"✅ Chapter {cid} completed!")
    return ch_mp3

async def main():
    tasks = [synthesize_chapter(ch) for ch in chapters]
    ch_files = await asyncio.gather(*tasks)
    
    print("\nConcatenating 10 chapter MP3 files into final 30-min MP3...")
    with open(final_mp3_path, 'wb') as outfile:
        for fpath in sorted(ch_files, key=lambda x: int(re.search(r'ch_(\d+)', x).group(1))):
            with open(fpath, 'rb') as infile:
                outfile.write(infile.read())
                
    size_mb = os.path.getsize(final_mp3_path) / (1024 * 1024)
    print(f"\n🎉 ALL 10 CHAPTERS SYNTHESIZED! Final Neural Broadcast MP3: {final_mp3_path} ({size_mb:.2f} MB)")

if __name__ == '__main__':
    asyncio.run(main())
