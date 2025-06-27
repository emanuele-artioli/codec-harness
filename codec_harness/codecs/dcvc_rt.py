import subprocess
import os
from .base_codec import BaseCodec
from typing import Dict, Any

class DCVCRTCodec(BaseCodec):
    """Codec plugin for Microsoft's DCVC-RT neural codec."""

    @property
    def name(self) -> str:
        return "dcvc-rt"

    def get_supported_options(self) -> Dict[str, Any]:
        return {
            'quality': 3,  # 1-6, lower is higher bitrate
            'model': 'DCVC-RT', # or DCVC-RT-light, DCVC-RT-tiny
        }

    def encode(self, frame_input_dir: str, output_path: str, options: Dict[str, Any]) -> None:
        merged_options = {**self.get_supported_options(), **options}
        quality = merged_options['quality']
        model_name = merged_options['model']
        
        dcvc_repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'vendor', 'DCVC'))
        dcvc_script = os.path.join(dcvc_repo_path, 'test.py')
        
        # DCVC works on video files, not frames. We first need to re-assemble the frames
        # into a lossless video for DCVC to process.
        temp_input_video = os.path.join(os.path.dirname(output_path), "temp_dcvc_input.mp4")
        
        ffmpeg_command = [
            'ffmpeg', '-y', '-framerate', '30', '-i', f'{frame_input_dir}/frame_%05d.png',
            '-c:v', 'libx264', '-crf', '0', temp_input_video
        ]
        subprocess.run(ffmpeg_command, check=True, capture_output=True, text=True)

        print(f"Encoding with {self.name}...")
        
        # The output of DCVC's script is a directory with the bitstream and reconstructed video
        # We'll point it to a temp directory and then copy the final bitstream
        output_dir = os.path.dirname(output_path)
        output_name = os.path.splitext(os.path.basename(output_path))[0]

        command = [
            'python', dcvc_script,
            '--video_path', temp_input_video,
            '--model', model_name,
            '--quality', str(quality),
            '--save_dir', output_dir,
            '--output_name', output_name,
        ]

        try:
            # Note: DCVC scripts may need to be run from their own directory
            subprocess.run(command, check=True, capture_output=True, text=True, cwd=dcvc_repo_path)
            # The actual output file will be something like output_dir/output_name.bin
            # For simplicity, we assume this. A real implementation might need to rename it.
            print(f"Successfully encoded with DCVC-RT. Bitstream at {output_dir}/{output_name}.bin")
        except subprocess.CalledProcessError as e:
            print(f"Error during DCVC-RT encoding:\nCommand: {' '.join(e.cmd)}\nStderr: {e.stderr}")
            raise
        finally:
            os.remove(temp_input_video)