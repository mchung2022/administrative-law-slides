import re

with open('index.html', 'r', encoding='utf8') as f:
    text = f.read()

# Find all slide blocks and check podcastScript presence
slides_with_podcast = []
slides_without_podcast = []

# Regex to capture slide IDs and whether podcastScript is present before next slide ID
matches = re.finditer(r'{\s*"id":\s*(\d+)[\s\S]*?}(?=\s*,\s*{\s*"id":|\s*\])', text)

for m in matches:
    block = m.group(0)
    sid_match = re.search(r'"id":\s*(\d+)', block)
    if sid_match:
        sid = int(sid_match.group(1))
        if '"podcastScript"' in block:
            slides_with_podcast.append(sid)
        else:
            slides_without_podcast.append(sid)

print(f"Slides WITH podcastScript: {len(slides_with_podcast)}")
if slides_with_podcast:
    print(f"Range with podcast: {min(slides_with_podcast)} - {max(slides_with_podcast)}")

print(f"Slides WITHOUT podcastScript: {len(slides_without_podcast)}")
if slides_without_podcast:
    print(f"Missing slides sample: {slides_without_podcast[:20]} ... {slides_without_podcast[-10:]}")
