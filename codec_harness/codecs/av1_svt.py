import subprocess
from .base_codec import BaseCodec
from typing import Dict, Any

class AV1SvtCodec(BaseCodec):
    """Codec plugin for AV1 using the libsvtav1 encoder in FFmpeg."""

    @property
    def name(self) -> str:
        return "libsvtav1"

    def get_supported_options(self) -> Dict[str, Any]:
        return {
            'preset': 8,                      # 0-12, higher is faster
            'video_bitrate': "1600k",         # e.g., "1600k", "2M"
            'gop_size': 50,                   # Keyframe interval
            'scale_height': 540,              # Vertical resolution, e.g., 540 for 540p
            'framerate': 30,
            'fragmented_mp4': True,           # Use movflags for streaming
        }

    def encode(self, frame_input_dir: str, output_path: str, options: Dict[str, Any]) -> None:
        # Note: This implementation only handles video encoding from frames.
        # The original command's audio options (-c:a, -b:a) are ignored as frames have no audio.
        merged_options = {**self.get_supported_options(), **options}

        print(f"Encoding with {self.name}...")
        print(f"Options: {merged_options}")

        command = [
            'ffmpeg', '-y',
            '-framerate', str(merged_options['framerate']),
            '-i', f'{frame_input_dir}/frame_%05d.png',
            '-vf', f"scale=-2:{merged_options['scale_height']}",
            '-c:v', self.name,
            '-preset', str(merged_options['preset']),
            '-b:v', str(merged_options['video_bitrate']),
            '-g', str(merged_options['gop_size']),
        ]

        if merged_options.get('fragmented_mp4', False):
            command.extend(['-movflags', 'frag_keyframe+empty_moov'])

        command.append(output_path)

        try:
            subprocess.run(command, check=True, capture_output=True, text=True)
            print(f"Successfully encoded video to {output_path}")
        except subprocess.CalledProcessError as e:
            print(f"Error during FFmpeg encoding with {self.name}:\nCommand: {' '.join(e.cmd)}\nStderr: {e.stderr}")
            raise