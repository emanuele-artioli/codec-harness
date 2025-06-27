import subprocess
from .base_codec import BaseCodec
from typing import Dict, Any

class H264FFmpegCodec(BaseCodec):
    """Codec plugin for H.264 using the libx264 encoder in FFmpeg."""

    @property
    def name(self) -> str:
        return "libx264"

    def get_supported__options(self) -> Dict[str, Any]:
        return {
            'crf': 23,  # Constant Rate Factor (0-51, lower is better quality)
            'preset': 'medium',  # Encoding speed vs. compression (e.g., 'slow', 'medium', 'fast')
            'framerate': 30,
        }

    def encode(self, frame_input_dir: str, output_path: str, options: Dict[str, Any]) -> None:
        merged_options = {**self.get_supported_options(), **options}

        crf = merged_options['crf']
        preset = merged_options['preset']
        framerate = merged_options['framerate']

        print(f"Encoding with {self.name}...")
        print(f"Options: crf={crf}, preset={preset}, framerate={framerate}")

        command = [
            'ffmpeg',
            '-y',  # Overwrite output file if it exists
            '-framerate', str(framerate),
            '-i', f'{frame_input_dir}/frame_%05d.png',
            '-c:v', 'libx264',
            '-preset', preset,
            '-crf', str(crf),
            '-pix_fmt', 'yuv420p',  # For compatibility
            output_path
        ]

        try:
            subprocess.run(command, check=True, capture_output=True, text=True)
            print(f"Successfully encoded video to {output_path}")
        except subprocess.CalledProcessError as e:
            print(f"Error during FFmpeg encoding with {self.name}:")
            print(f"Command: {' '.join(e.cmd)}")
            print(f"Stderr: {e.stderr}")
            raise