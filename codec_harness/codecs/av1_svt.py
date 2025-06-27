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
            'preset': 8,
            'video_bitrate': "1600k",
            'gop_size': 50,
            'scale_height': 540,
            'framerate': 30,
            'fragmented_mp4': True,
        }

    def encode(self, frame_input_dir: str, output_path: str, options: Dict[str, Any]) -> None:
        merged_options = {**self.get_supported_options(), **options}
        print(f"Encoding with {self.name}...")
        print(f"Options: {merged_options}")

        input_pattern = f'{frame_input_dir}/*.jpg'

        command = [
            'ffmpeg', '-y',
            '-framerate', str(merged_options['framerate']),
            '-pattern_type', 'glob', '-i', input_pattern,
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