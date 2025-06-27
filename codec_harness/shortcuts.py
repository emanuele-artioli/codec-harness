from codec_harness import encode
from typing import Literal

def encode_h264(
    input_path: str,
    output_path: str,
    crf: int = 23,
    preset: Literal[
        "ultrafast", "superfast", "veryfast", "faster", "fast",
        "medium", "slow", "slower", "veryslow", "placebo"
    ] = "medium",
    framerate: int = 30
):
    """A type-safe wrapper to encode a video using the libx264 codec."""
    encode(
        input_path, output_path, codec_name="libx264",
        crf=crf, preset=preset, framerate=framerate
    )

def encode_av1(
    input_path: str,
    output_path: str,
    preset: int = 8,
    video_bitrate: str = "1600k",
    gop_size: int = 50,
    scale_height: int = 540,
    framerate: int = 30,
    fragmented_mp4: bool = True
):
    """A type-safe wrapper to encode a video using the libsvtav1 codec."""
    encode(
        input_path, output_path, codec_name="libsvtav1",
        preset=preset, video_bitrate=video_bitrate, gop_size=gop_size,
        scale_height=scale_height, framerate=framerate, fragmented_mp4=fragmented_mp4
    )