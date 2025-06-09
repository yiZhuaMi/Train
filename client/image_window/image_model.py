import numpy as np
from typing import Optional

class ImageModel:
    def __init__(self):
        self.cv_image: np.ndarray | None = None

    def set_image(self, image: np.ndarray):
        self.cv_image = image
    
    def get_image(self) -> Optional[np.ndarray]:
        return self.cv_image