import os
import importlib
from .codecs.base_codec import BaseCodec
from typing import Dict, Type, List

class CodecManager:
    """Discovers, loads, and manages codec plugins."""

    def __init__(self, codec_dir: str = None):
        self.codecs: Dict[str, Type[BaseCodec]] = {}
        # If no dir is provided, find the 'codecs' sub-package within this package
        if codec_dir is None:
            codec_dir = os.path.join(os.path.dirname(__file__), "codecs")
        self._load_plugins(codec_dir, 'codec_harness.codecs')

    def _load_plugins(self, codec_dir: str, package_name: str):
        for filename in os.listdir(codec_dir):
            if filename.endswith(".py") and not filename.startswith("__"):
                module_name = f".{filename[:-3]}"
                try:
                    # Use relative import for plugins within the package
                    module = importlib.import_module(module_name, package=package_name)
                    for attr_name in dir(module):
                        attr = getattr(module, attr_name)
                        if isinstance(attr, type) and issubclass(attr, BaseCodec) and attr is not BaseCodec:
                            instance = attr()
                            self.codecs[instance.name] = attr
                            print(f"Discovered and loaded codec: {instance.name}")
                except Exception as e:
                    print(f"Could not load plugin from {filename}: {e}")

    def get_codec(self, name: str) -> Type[BaseCodec]:
        """Returns the codec class for the given name."""
        codec_class = self.codecs.get(name)
        if not codec_class:
            raise ValueError(f"Codec '{name}' not found. Available codecs: {list(self.codecs.keys())}")
        return codec_class

    def list_codecs(self) -> List[str]:
        """Returns a list of names of all available codecs."""
        return list(self.codecs.keys())