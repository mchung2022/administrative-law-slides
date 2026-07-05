import asyncio
import edge_tts

async def main():
    voices = await edge_tts.VoicesManager.create()
    tw_voices = voices.find(Language='zh', Locale='zh-TW')
    print("=== Available Traditional Chinese Professional Neural Voices ===")
    for v in tw_voices:
        print(f"- {v['ShortName']} ({v['Gender']})")

if __name__ == '__main__':
    asyncio.run(main())
