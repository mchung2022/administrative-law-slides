import os
import wave
import struct

path = os.path.join(os.path.dirname(__file__), '..', 'podcast_audio_30min.wav')

if not os.path.exists(path):
    print("❌ File not found:", path)
    exit(1)

with wave.open(path, 'rb') as wf:
    nchannels = wf.getnchannels()
    sampwidth = wf.getsampwidth()
    framerate = wf.getframerate()
    nframes = wf.getnframes()
    duration = nframes / float(framerate)
    print(f"Channels: {nchannels}, SampleWidth: {sampwidth}, FrameRate: {framerate}, NFrames: {nframes}, Duration: {duration:.2f} seconds ({duration/60:.2f} mins)")
    
    frames = wf.readframes(nframes)
    if sampwidth == 2:
        samples = struct.unpack(f'<{len(frames)//2}h', frames)
        max_amp = max(abs(s) for s in samples)
        min_amp = min(samples)
        non_zero = sum(1 for s in samples if s != 0)
        print(f"Max Amplitude: {max_amp}, Min Amplitude: {min_amp}, Non-Zero Samples: {non_zero}/{len(samples)}")
        if max_amp == 0:
            print("❌ WARNING: AUDIO IS COMPLETELY SILENT (ALL ZEROES)!")
        else:
            print(f"✅ AUDIO CONTAINS SOUND DATA! (Max Amp: {max_amp})")
