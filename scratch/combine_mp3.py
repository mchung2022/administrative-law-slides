import os
import re

print("=== Concatenating 10 Professional Neural Broadcast MP3 Chapters ===")

output_dir = os.path.join(os.path.dirname(__file__), 'ch_audio')
final_mp3_path = os.path.join(os.path.dirname(__file__), '..', 'podcast_audio_30min.mp3')

files = [f for f in os.listdir(output_dir) if f.startswith('ch_') and f.endswith('.mp3')]
files = sorted(files, key=lambda x: int(re.search(r'ch_(\d+)', x).group(1)))

print(f"Combining {len(files)} files in exact order: {files}")

with open(final_mp3_path, 'wb') as outfile:
    for fname in files:
        fpath = os.path.join(output_dir, fname)
        with open(fpath, 'rb') as infile:
            outfile.write(infile.read())

size_mb = os.path.getsize(final_mp3_path) / (1024 * 1024)
print(f"✅ Final Neural Broadcast MP3 Successfully Created: {final_mp3_path} ({size_mb:.2f} MB)")
