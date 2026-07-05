import os
import json
import re
import asyncio
import edge_tts

print("=== Synthesizing Professional Broadcast Host Neural Audio (zh-TW-YunJheNeural) ===")

json_path = os.path.join(os.path.dirname(__file__), 'podcast_script_30min.json')
mp3_output_path = os.path.join(os.path.dirname(__file__), '..', 'podcast_audio_30min.mp3')
wav_output_path = os.path.join(os.path.dirname(__file__), '..', 'podcast_audio_30min.wav')

with open(json_path, 'r', encoding='utf8') as f:
    chapters = json.load(f)

# Concatenate full spoken text with natural pauses between chapters
full_spoken_segments = []

for ch in chapters:
    raw_text = ch['script']
    # Remove stage notes in brackets
    clean_text = re.sub(r'【.*?】', '', raw_text)
    clean_text = re.sub(r'（.*?）', '', clean_text)
    clean_text = clean_text.strip()
    full_spoken_segments.append(clean_text)

full_script_text = "\n\n......\n\n".join(full_spoken_segments)

VOICE = "zh-TW-YunJheNeural"  # Professional Male Broadcast Host Voice

async def generate_audio():
    print(f"Using Neural Voice: {VOICE}")
    print(f"Total Text Length to Synthesize: {len(full_script_text)} characters")
    
    communicate = edge_tts.Communicate(full_script_text, VOICE, rate="+0%", volume="+0%")
    
    print(f"Synthesizing MP3 Broadcast Audio: {mp3_output_path} ...")
    await communicate.save(mp3_output_path)
    print(f"✅ Neural Broadcast MP3 Successfully Created: {mp3_output_path}")

if __name__ == '__main__':
    asyncio.run(generate_audio())
