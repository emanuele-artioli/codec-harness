# Modular Video Codec Harness

A flexible, plugin-driven Python package to encode videos with a range of codecs, from traditional (H.264, AV1) to state-of-the-art neural codecs (DCVC-RT, Hi-NeRV).

## WARNING: System Requirements for Neural Codecs

Neural codecs are computationally intensive and **require a modern NVIDIA GPU with CUDA installed.**

---

### **Installation for Development**

1.  **Clone the repository:**
    ```sh
    git clone <your-repo-url>
    cd video-codec-harness
    ```

2.  **Initialize Git Submodules:**
    This step is crucial. It downloads the source code for the neural codecs into the `vendor/` directory.
    ```sh
    git submodule update --init --recursive
    ```

3.  **Create and activate the Conda environment:**
    This command reads the `environment.yml` file, installs all dependencies (`ffmpeg`, `PyTorch`, `CUDA`), and installs the `codec-harness` package in editable mode.
    ```sh
    conda env create -f environment.yml
    conda activate codec-harness-env
    ```
    
4.  **Install Submodule Dependencies:**
    Some submodules may have their own dependencies.
    ```sh
    pip install -e vendor/DCVC
    pip install -e vendor/HiNeRV 
    ```

---

### **How to Use**

1. **As a Command-Line Tool**
    ```sh
    # Example for DCVC-RT
    codec-harness \
    --input /path/to/video.mp4 \
    --output /path/to/dcvc_out.bin \
    --codec dcvc-rt \
    --codec-options "quality=3,model=DCVC-RT"
    ```

2. **As a Library in Another Project**

    *Style A: Using a Convenience Shortcut (Recommended)*

    This method is best for discoverability and type safety. Your IDE will provide autocompletion and error checking.

    (in my_other_project.py)

    from codec_harness.shortcuts import encode_h264
    try:
        encode_h264(
            input_path="videos/raw.mp4",
            output_path="videos/encoded_h264.mp4",
            crf=28,
            preset="veryfast"
        )
        print("Video encoded successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")

    *Style B: Using the Core encode Function*

    This method is best when the codec is determined at runtime (e.g., from a config file or user input).

    (in my_other_project.py)

    from codec_harness import encode
    Codec could come from a config file, user input, etc.
    codec_to_use = "libx264" 
    options = {"crf": 23, "preset": "medium"}
    try:
        encode(
            input_path="videos/raw.mp4",
            output_path="videos/encoded_dynamic.mp4",
            codec_name=codec_to_use,
            **options
        )
        print("Video encoded successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")

### **How to Add a New Codec**
    Create the plugin file in the codec_harness/codecs/ directory (e.g., my_new_codec.py).

    Create a class in that file that inherits from codec_harness.codecs.base_codec.BaseCodec.

    Implement the required properties and methods (name, get_supported_options, encode).

    Update environment.yml if your codec has new dependencies.

    Re-create the Conda environment or rebuild the Docker image. The CodecManager will automatically discover your new codec.