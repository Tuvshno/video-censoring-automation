import subprocess

def mute_sections(audio_file_path, timestamps, output_file_path):
    # Construct the volume filter command for each timestamp range
    volume_filters = [
        f"volume=enable='between(t,{start},{end})':volume=0" for start, end in timestamps
    ]
    
    # Join all volume filters with a comma to chain them together
    filters_string = ', '.join(volume_filters)

    # Construct the FFmpeg command
    ffmpeg_cmd = [
        "ffmpeg",
        "-i", audio_file_path,
        "-af", filters_string,
        "-y",
        output_file_path
    ]

    # Print the FFmpeg command for debugging
    print("Executing FFmpeg command:", " ".join(ffmpeg_cmd))

    # Execute the FFmpeg command
    result = subprocess.run(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # Print FFmpeg output and errors
    print("FFmpeg Output:", result.stdout)
    print("FFmpeg Errors:", result.stderr)