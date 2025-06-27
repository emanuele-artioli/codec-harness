import os
import subprocess
import tempfile

class InputHandler:
    """Handles preparation of input data for encoding."""

    def prepare_frames(self, input_path: str) -> str:
        """
        Ensures input is a directory of frames. If input is a video,
        it extracts frames to a temporary directory.

        Args:
            input_path (str): Path to a video file or a directory of frames.

        Returns:
            str: Path to the directory containing frames.
        """
        if os.path.isdir(input_path):
            print("Input is a directory of frames. Skipping extraction.")
            return input_path

        if os.path.isfile(input_path):
            print(f"Input is a video file. Extracting frames...")
            temp_dir = tempfile.mkdtemp(prefix="codec_harness_frames_")
            output_pattern = os.path.join(temp_dir, "frame_%05d.png")

            command = ['ffmpeg', '-i', input_path, output_pattern]

            try:
                subprocess.run(command, check=True, capture_output=True, text=True)
                print(f"Frames extracted to temporary directory: {temp_dir}")
                return temp_dir
            except subprocess.CalledProcessError as e:
                print(f"Error extracting frames with FFmpeg:\nCommand: {' '.join(e.cmd)}\nStderr: {e.stderr}")
                raise
        
        raise FileNotFoundError(f"Input path {input_path} is not a valid file or directory.")