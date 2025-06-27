import argparse
import sys
from codec_harness import encode

def parse_codec_options(options_str: str) -> dict:
    if not options_str:
        return {}
    try:
        return {key.strip(): value.strip() for key, value in (item.split('=') for item in options_str.split(','))}
    except ValueError:
        raise argparse.ArgumentTypeError("Codec options must be 'key1=value1,key2=value2'.")

def main():
    parser = argparse.ArgumentParser(description="Modular Video Codec Harness")
    parser.add_argument("-i", "--input", required=True, help="Path to input video file or directory of frames.")
    parser.add_argument("-o", "--output", required=True, help="Path for the output encoded file.")
    parser.add_argument("-c", "--codec", required=True, help="Codec to use for encoding.")
    parser.add_argument("--codec-options", type=parse_codec_options, default={}, help="Comma-separated key=value pairs for codec options.")
    
    args = parser.parse_args()

    try:
        encode(
            input_path=args.input,
            output_path=args.output,
            codec_name=args.codec,
            **args.codec_options
        )
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()