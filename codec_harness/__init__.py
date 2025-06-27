from .codec_manager import CodecManager
from .input_handler import InputHandler

def encode(input_path: str, output_path: str, codec_name: str, **codec_options):
    """
    High-level function to encode a video. This is the primary entry point
    for using this package as a library.

    Args:
        input_path (str): Path to the input video file or frame directory.
        output_path (str): Path for the encoded output file.
        codec_name (str): The name of the codec to use (e.g., 'libx264').
        **codec_options: Arbitrary keyword arguments for codec-specific options.
    """
    print(f"Starting encoding process for {input_path}...")
    
    handler = InputHandler()
    frame_dir = handler.prepare_frames(input_path)
    
    manager = CodecManager()
    codec_class = manager.get_codec(codec_name)
    codec_instance = codec_class()

    codec_instance.encode(frame_dir, output_path, codec_options)
    print("Encoding process completed successfully.")