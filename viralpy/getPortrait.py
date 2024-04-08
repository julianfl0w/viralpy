import subprocess
import sys
import os

def calculate_crop_parameters(video_width, video_height, target_width, target_height, offset):
    # Calculate the scaling factor to maintain aspect ratio
    scale_factor = min(video_height / target_height, video_width / target_width)

    # Calculate new dimensions that fit into the video
    new_width = int(scale_factor * target_width)
    new_height = int(scale_factor * target_height)

    # Calculate the position for cropping
    x_offset = max(0, min(video_width - new_width, offset))
    y_offset = max(0, min(video_height - new_height, offset))

    return new_width, new_height, x_offset, y_offset

def crop_video(input_file, output_file, target_width=1080, target_height=1920, offset=0):
    # Get video dimensions
    cmd = ['ffprobe', '-v', 'error', '-select_streams', 'v:0',
           '-show_entries', 'stream=width,height', '-of', 'csv=p=0', input_file]
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    video_width, video_height = map(int, proc.stdout.strip().split(','))

    # Calculate crop parameters
    crop_width, crop_height, x_offset, y_offset = calculate_crop_parameters(
        video_width, video_height, target_width, target_height, offset)

    # Construct FFmpeg command for cropping
    ffmpeg_cmd = [
        'ffmpeg',
        '-i', input_file,
        '-vf', f'crop={crop_width}:{crop_height}:{x_offset}:{y_offset}',
        '-c:a', 'copy',  # Copy audio without changes
        output_file
    ]

    # Execute the FFmpeg command
    subprocess.run(ffmpeg_cmd, check=True)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <input_video> [offset]")
        sys.exit(1)

    input_video = sys.argv[1]
    offset = int(sys.argv[2]) if len(sys.argv) > 2 else 0  # Optional offset parameter
    base_name, ext = os.path.splitext(os.path.basename(input_video))
    output_video = f"{base_name}_pcrop{ext}"

    crop_video(input_video, output_video, offset=offset)

    print(f"Cropped video saved as: {output_video}")
