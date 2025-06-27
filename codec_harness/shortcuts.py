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
    """
    A type-safe wrapper to encode a video using the libx264 codec.

    Args:
        input_path (str): Path to the input video file or frame directory.
        output_path (str): Path for the encoded output file.
        crf (int): Constant Rate Factor (0-51). Lower is better quality. Defaults to 23.
        preset (str): Encoding speed vs. compression. Defaults to 'medium'.
        framerate (int): Output framerate. Defaults to 30.
    """
    encode(
        input_path,
        output_path,
        codec_name="libx264",
        crf=crf,
        preset=preset,
        framerate=framerate
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
    """
    A type-safe wrapper to encode a video using the libsvtav1 codec.

    Args:
        input_path (str): Path to the input video file or frame directory.
        output_path (str): Path for the encoded output file.
        preset (int): Encoding speed (0-12), higher is faster. Defaults to 8.
        video_bitrate (str): Target video bitrate (e.g., "1600k", "2M"). Defaults to "1600k".
        gop_size (int): Group of Pictures (keyframe interval). Defaults to 50.
        scale_height (int): Target vertical resolution. Defaults to 540.
        framerate (int): Output framerate. Defaults to 30.
        fragmented_mp4 (bool): Use movflags for fragmented MP4 output. Defaults to True.
    """
    encode(
        input_path, output_path, codec_name="libsvtav1",
        preset=preset, video_bitrate=video_bitrate, gop_size=gop_size,
        scale_height=scale_height, framerate=framerate, fragmented_mp4=fragmented_mp4
    )

def encode_dcvc_rt(
    input_path: str,
    output_path: str,
    quality: int = 3,
    model: Literal['DCVC-RT', 'DCVC-RT-light', 'DCVC-RT-tiny'] = 'DCVC-RT'
):
    """A type-safe wrapper to encode a video using the DCVC-RT codec."""
    encode(
        input_path, output_path, codec_name="dcvc-rt",
        quality=quality, model=model
    )

def encode_hinerv(
    input_path: str,
    output_path: str,
    model_size: Literal['s', 'm', 'l'] = 's',
    epochs: int = 300
):
    """A type-safe wrapper to encode a video by overfitting a Hi-NeRV model."""
    encode(
        input_path, output_path, codec_name="hinerv",
        model_size=model_size, epochs=epochs
    )

# To add another shortcut (e.g., for a hypothetical AV1 codec):
#
# def encode_av1(input_path: str, output_path: str, cpu_used: int = 4, ...):
#     encode(
#         input_path,
#         output_path,
#         codec_name="libsvtav1",
#         cpu_used=cpu_used,
#         ...
#     )