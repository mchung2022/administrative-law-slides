import os
import asyncio
import edge_tts
from measure_mp3_duration import get_mp3_duration

print("=== Calibrating Natural Adult Daily Speech Rate ===")

test_text = "哈囉各位同學！歡迎來到今天的行政法 Podcast 廣播對談講堂。今天我們要探討的主題是依法行政原則與層次化法律保留。"

async def run_test():
    for r in ["-10%", "-15%", "-20%"]:
        mp3_out = f"scratch/rate_test_{r.replace('-','')}.mp3"
        comm = edge_tts.Communicate(test_text, "zh-TW-YunJheNeural", rate=r)
        await comm.save(mp3_out)
        dur = get_mp3_duration(mp3_out)
        cps = len(test_text) / dur if dur > 0 else 0
        print(f"Rate '{r}': Duration = {dur:.2f}s | Speed = {cps:.2f} chars/sec ({cps*60:.0f} chars/min)")
        await asyncio.sleep(0.5)

if __name__ == '__main__':
    asyncio.run(run_test())
