import os
import json
import re
import asyncio
import edge_tts
from pydub import AudioSegment

async def main():
    json_path = os.path.join(os.path.dirname(__file__), 'podcast_script_30min.json')
    with open(json_path, 'r', encoding='utf8') as f:
        chapters = json.load(f)
        
    ch1 = chapters[0]['script']
    clean_text = re.sub(r'【.*?】', '', ch1)
    clean_text = re.sub(r'（.*?）', '', clean_text).strip()
    
    # Test rate="-35%"
    test_file = "test_ch1_rate35.mp3"
    comm = edge_tts.Communicate(clean_text, "zh-TW-HsiaoChenNeural", rate="-35%")
    await comm.save(test_file)
    
    # Check duration with mutagen or pydub if available, or reading mp3 frames
    size_bytes = os.path.getsize(test_file)
    print(f"Rate -35% test file size: {size_bytes / 1024:.1f} KB")

if __name__ == '__main__':
    asyncio.run(main())
