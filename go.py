import os
import subprocess

source = r"Y:\stream\split"
dest = r"Y:\stream"

segment_time = 41400  # 11.5시간 (초 단위)
mkv_files = [f for f in os.listdir(source) if f.endswith(".mkv")]

for mkv_file in mkv_files:
    input_path = os.path.join(source, mkv_file)
    file_name, _ = os.path.splitext(mkv_file)
    output_pattern = os.path.join(dest, f"{file_name}_part%d.mkv")
    cmd = [
        "ffmpeg", "-i", input_path, "-c", "copy", "-map", "0",
        "-f", "segment", "-segment_time", str(segment_time),
        "-reset_timestamps", "1", output_pattern,
        "-loglevel", "warning", "-stats"
    ]
    print(f"Processing: {mkv_file} -> {output_pattern}")
    result = subprocess.run(cmd, check=True)

    if result.returncode == 0:
        try:
            os.remove(input_path)
        except Exception as e:
            print(f"파일 삭제 실패: {input_path} 오류 내용: ({e})")
            
print("Done.")
