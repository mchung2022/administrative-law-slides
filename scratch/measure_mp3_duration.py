import os
import struct

def get_mp3_duration(file_path):
    # Parse MP3 frame headers
    bitrates = [
        [0, 32, 64, 96, 128, 160, 192, 224, 256, 288, 320, 352, 384, 416, 448], # V1, L1
        [0, 32, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320, 384],     # V1, L2
        [0, 32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320],     # V1, L3
        [0, 32, 48, 56, 64, 80, 96, 112, 128, 144, 160, 175, 192, 224, 256],     # V2, L1
        [0, 8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 144, 160]          # V2, L2/L3
    ]
    sample_rates = [
        [44100, 48000, 32000], # V1
        [22050, 24000, 16000], # V2
        [11025, 12000, 8000]   # V2.5
    ]

    with open(file_path, 'rb') as f:
        data = f.read()

    size = len(data)
    i = 0
    total_samples = 0
    sample_rate = 24000
    
    while i < size - 4:
        if data[i] == 0xFF and (data[i+1] & 0xE0) == 0xE0:
            header = struct.unpack('>I', data[i:i+4])[0]
            version = (header >> 19) & 0x03 # 3=V1, 2=V2, 0=V2.5
            layer = (header >> 17) & 0x03   # 3=L1, 2=L2, 1=L3
            bitrate_idx = (header >> 12) & 0x0F
            sr_idx = (header >> 10) & 0x03
            padding = (header >> 9) & 0x01

            if version != 1 and layer == 1 and sr_idx < 3 and bitrate_idx < 15:
                # MPEG 1 or 2 Layer III
                v_idx = 0 if version == 3 else 1
                sr = sample_rates[v_idx][sr_idx]
                sample_rate = sr
                br = bitrates[2 if version==3 else 4][bitrate_idx] * 1000
                if br > 0 and sr > 0:
                    frame_len = int(144 * br / sr) + padding
                    if frame_len > 0:
                        total_samples += 1152
                        i += frame_len
                        continue
        i += 1

    duration = total_samples / float(sample_rate) if sample_rate else 0
    return duration

if __name__ == '__main__':
    for fname in os.listdir('.'):
        if fname.endswith('.mp3'):
            dur = get_mp3_duration(fname)
            print(f"{fname}: {dur:.2f} seconds ({dur/60:.2f} mins)")
