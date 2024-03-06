import subprocess

def resize_video(input_file, output_file, target_width=1080, target_height=1920):
    # Construct FFmpeg command for resizing and padding to maintain aspect ratio
    ffmpeg_cmd = [
        'ffmpeg',
        '-i', input_file,
        '-vf', f'scale={target_width}:{target_height}:force_original_aspect_ratio=decrease,pad={target_width}:{target_height}:(ow-iw)/2:(oh-ih)/2',
        '-c:a', 'copy',  # Copy audio without changes
        output_file
    ]

    # Execute the FFmpeg command
    subprocess.run(ffmpeg_cmd, check=True)

if __name__ == "__main__":
    input_video = 'users_cropped_pcrop.mp4'
    output_video = 'users_resized.mp4'
    
    resize_video(input_video, output_video)

    print(f"Resized video saved as: {output_video}")
