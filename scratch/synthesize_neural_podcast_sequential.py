import os
import json
import re
import asyncio
import edge_tts

print("=== Sequential Professional Neural Broadcast Voice Synthesis with Retry Logic ===")

json_path = os.path.join(os.path.dirname(__file__), 'podcast_script_30min.json')
output_dir = os.path.join(os.path.dirname(__file__), 'ch_audio')
os.makedirs(output_dir, exist_ok=True)

final_mp3_path = os.path.join(os.path.dirname(__file__), '..', 'podcast_audio_30min.mp3')

with open(json_path, 'r', encoding='utf8') as f:
    chapters = json.load(f)

# zh-TW-HsiaoChenNeural (Female Broadcast Host) or zh-TW-YunJheNeural (Male Broadcast Host)
VOICE = "zh-TW-HsiaoChenNeural"

async def synthesize_one_chapter(ch):
    cid = ch['id']
    raw_text = ch['script']
    clean_text = re.sub(r'【.*?】', '', raw_text)
    clean_text = re.sub(r'（.*?）', '', clean_text).strip()
    
    ch_mp3 = os.path.join(output_dir, f"ch_{cid}.mp3")
    print(f"[Chapter {cid}/10] Synthesizing {len(clean_text)} chars with {VOICE}...")
    
    for attempt in range(1, 4):
        try:
            communicate = edge_tts.Communicate(clean_text, VOICE, rate="+0%", volume="+0%")
            await communicate.save(ch_mp3)
            size_kb = os.path.getsize(ch_mp3) / 1024
            if size_kb > 10:
                print(f"[OK] Chapter {cid} completed successfully ({size_kb:.1f} KB).")
                return ch_mp3
        except Exception as e:
            print(f"⚠️ Attempt {attempt} failed for Chapter {cid}: {e}. Retrying in 2s...")
            await asyncio.sleep(2.0)
            
    raise Exception(f"❌ Failed to synthesize Chapter {cid} after 3 attempts!")

async def main():
    ch_files = []
    for ch in chapters:
        fpath = await synthesize_one_chapter(ch)
        ch_files.append(fpath)
        await asyncio.sleep(1.5)

    print("\nCombining 10 chapter MP3 files into podcast_audio_30min.mp3...")
    with open(final_mp3_path, 'wb') as outfile:
        for fpath in ch_files:
            with open(fpath, 'rb') as infile:
                outfile.write(infile.read())
                
    size_mb = os.path.getsize(final_mp3_path) / (1024 * 1024)
    print(f"[OK] Final Professional Neural Broadcast MP3 created: {final_mp3_path} ({size_mb:.2f} MB)")

if __name__ == '__main__':
    asyncio.run(main())
