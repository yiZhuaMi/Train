import numpy as np
from typing import Optional

from .annotated_image import AnnotatedImage

class ImageModel:
    def __init__(self):
        self.cv_image: np.ndarray | None = None
        self.annoteted_image: AnnotatedImage

    def set_image(self, image: np.ndarray):
        self.cv_image = image

    def set_annoteted_image(self, annotated_image: AnnotatedImage):
        self.annoteted_image = annotated_image
    
    def get_image(self) -> Optional[np.ndarray]:
        return self.cv_image
    
    def get_annotated_image(self) -> AnnotatedImage:
        return self.annoteted_image