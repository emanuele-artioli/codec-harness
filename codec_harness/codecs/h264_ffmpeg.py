import subprocess
from .base_codec import BaseCodec
from typing import Dict, Any

class H264FFmpegCodec(BaseCodec):
    """Codec plugin for H.264 using the libx264 encoder in FFmpeg."""

    @property
    def name(self) -> str:
        return "libx264"

    def get_supported_options(self) -> Dict[str, Any]:
        return {
            'crf': 23,
            'preset': 'medium',
            'framerate': 30,
        }

    def encode(self, frame_input_dir: str, output_path: str, options: Dict[str, Any]) -> None:
        merged_options = {**self.get_supported_options(), **options}
        crf = merged_options['crf']
        preset = merged_options['preset']
        framerate = merged_options['framerate']

        print(f"Encoding with {self.name}...")
        print(f"Options: crf={crf}, preset={preset}, framerate={framerate}")

        input_pattern = f'{frame_input_dir}/*.jpg'

        command = [
            'ffmpeg', '-y', '-framerate', str(framerate),
            '-pattern_type', 'glob', '-i', input_pattern,
            '-c:v', 'libx264', '-preset', preset, '-crf', str(crf),
            '-pix_fmt', 'yuv420p', output_path
        ]
        try:
            subprocess.run(command, check=True, capture_output=True, text=True)
            print(f"Successfully encoded video to {output_path}")
        except subprocess.CalledProcessError as e:
            print(f"Error during FFmpeg encoding with {self.name}:\nCommand: {' '.join(e.cmd)}\nStderr: {e.stderr}")
            raise