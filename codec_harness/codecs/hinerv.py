import subprocess
import os
from .base_codec import BaseCodec
from typing import Dict, Any

class HiNeRVCodec(BaseCodec):
    """Codec plugin for the Hi-NeRV neural codec."""

    @property
    def name(self) -> str:
        return "hinerv"

    def get_supported_options(self) -> Dict[str, Any]:
        return {
            'model_size': 's',  # 's', 'm', 'l' for small, medium, large
            'epochs': 300
        }

    def encode(self, frame_input_dir: str, output_path: str, options: Dict[str, Any]) -> None:
        merged_options = {**self.get_supported_options(), **options}
        model_size = merged_options['model_size']
        epochs = merged_options['epochs']

        hinerv_repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'vendor', 'HiNeRV'))
        hinerv_script = os.path.join(hinerv_repo_path, 'hinerv_main.py')
        
        model_cfg_path = os.path.join(hinerv_repo_path, f'cfgs/models/uvg-hinerv-{model_size}_1920x1080.txt')
        train_cfg_path = os.path.join(hinerv_repo_path, 'cfgs/train/hinerv_1920x1080.txt')

        print(f"Encoding (overfitting) with {self.name}...")

        command = [
            'accelerate', 'launch', hinerv_script,
            '--dataset', frame_input_dir,
            '--dataset-name', 'custom', # Tells script to just use the folder
            '--output', os.path.dirname(output_path),
            '--train-cfg-txt', train_cfg_path,
            '--model-cfg-txt', model_cfg_path,
            '--epochs', str(epochs),
            # Add other necessary args from HiNeRV repo
        ]

        try:
            # HiNeRV also needs to be run from its directory
            subprocess.run(command, check=True, capture_output=True, text=True, cwd=hinerv_repo_path)
            # The output will be a model checkpoint in the output directory.
            # For a true codec, you'd then run a compression/quantization script
            # and save the final bitstream to `output_path`.
            print(f"Successfully overfitted with HiNeRV. Model checkpoint saved in {os.path.dirname(output_path)}")
        except subprocess.CalledProcessError as e:
            print(f"Error during HiNeRV overfitting:\nCommand: {' '.join(e.cmd)}\nStderr: {e.stderr}")
            raise