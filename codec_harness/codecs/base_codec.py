from abc import ABC, abstractmethod
from typing import Dict, Any, List

class BaseCodec(ABC):
    """
    Abstract Base Class for all codec implementations.
    Each codec plugin must inherit from this class.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """A unique, lower-case name for the codec (e.g., 'libx264')."""
        pass

    @abstractmethod
    def get_supported_options(self) -> Dict[str, Any]:
        """
        Returns a dictionary of options supported by the codec,
        with default values.
        Example: {'crf': 23, 'preset': 'medium'}
        """
        pass

    @abstractmethod
    def encode(self, frame_input_dir: str, output_path: str, options: Dict[str, Any]) -> None:
        """
        Encodes a sequence of frames into a video file.

        Args:
            frame_input_dir (str): Path to the directory containing input frames
                                   (e.g., 'frame_%04d.png').
            output_path (str): Path to write the encoded video file.
            options (Dict[str, Any]): A dictionary of codec-specific options
                                      to override the defaults.
        """
        pass