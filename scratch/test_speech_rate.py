import os
import asyncio
import edge_tts
from measure_mp3_duration import get_mp3_duration

print("=== Testing Speech Pacing for Natural Adult Daily Speech Rate ===")

test_text = "哈囉各位同學！歡迎來到今天的行政法 Podcast 廣播對談講堂。今天我們要探討的主題是依法行政原則與層次化法律保留。"
print(f"Test text length: {len(test_text)} characters")

async def test_rates():
    rates = ["+0%", "-10%", "-15%", "-20%", "-30%"]
    for r in rates:
        mp3_out = f"scratch/test_rate_{r.replace('%','').replace('+','p')}.mp3"
        comm = edge_tts.Communicate(test_text, "zh-TW-YunJheNeural", rate=r)
        await comm.save(mp3_out)
        dur = get_mp3_duration(mp3_out)
        cps = len(test_text) / dur if dur > 0 else 0
        print(f"Rate '{r}': Duration = {dur:.2f}s | Speed = {cps:.2f} chars/sec ({cps*60:.0f} chars/min)")

if __name__ == '__main__':
    asyncio.run(test_rates())
