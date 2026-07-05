import os
import json
import re
import asyncio
import edge_tts

print("=== Generating 30-Min Professional Neural Broadcast Voice Podcast ===")

json_path = os.path.join(os.path.dirname(__file__), 'podcast_script_30min.json')
output_dir = os.path.join(os.path.dirname(__file__), 'ch_audio')
os.makedirs(output_dir, exist_ok=True)

final_mp3_path = os.path.join(os.path.dirname(__file__), '..', 'podcast_audio_30min.mp3')

with open(json_path, 'r', encoding='utf8') as f:
    chapters = json.load(f)

# zh-TW-YunJheNeural (Male Broadcast Host) or zh-TW-HsiaoChenNeural (Female Broadcast Host)
VOICE = "zh-TW-YunJheNeural"

async def main():
    ch_files = []
    for ch in chapters:
        cid = ch['id']
        raw_text = ch['script']
        clean_text = re.sub(r'【.*?】', '', raw_text)
        clean_text = re.sub(r'（.*?）', '', clean_text).strip()
        
        ch_mp3 = os.path.join(output_dir, f"ch_{cid}.mp3")
        print(f"[Chapter {cid}/10] Synthesizing {len(clean_text)} chars with {VOICE}...")
        
        communicate = edge_tts.Communicate(clean_text, VOICE, rate="+0%", volume="+0%")
        await communicate.save(ch_mp3)
        ch_files.append(ch_mp3)
        print(f"[OK] Chapter {cid} saved.")
        await asyncio.sleep(0.5)

    print("\nConcatenating chapter MP3 files into final 30-min MP3...")
    with open(final_mp3_path, 'wb') as outfile:
        for fpath in ch_files:
            with open(fpath, 'rb') as infile:
                outfile.write(infile.read())
                
    size_mb = os.path.getsize(final_mp3_path) / (1024 * 1024)
    print(f"[OK] Final Professional Neural Broadcast MP3 created: {final_mp3_path} ({size_mb:.2f} MB)")

if __name__ == '__main__':
    asyncio.run(main())
