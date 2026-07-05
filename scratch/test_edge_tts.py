import asyncio
import edge_tts

async def main():
    text = "各位同學們好！歡迎收聽行政法 500 頁旗艦總複習 30 分鐘特企 Podcast 廣播講堂！"
    voice = "zh-TW-HsiaoChenNeural"
    output = "test_speech.mp3"
    print(f"Testing TTS with voice {voice}...")
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output)
    print("✅ Successfully saved test_speech.mp3!")

if __name__ == '__main__':
    asyncio.run(main())
