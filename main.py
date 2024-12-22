import cv2
import numpy as np
from algo import edge_preserving_interpolation

if __name__ == '__main__':
    image = cv2.imread('istanbul.jpg')
    image = image.astype('int32')
    
    out = edge_preserving_interpolation(image, 4)
    
    cv2.imwrite('output.jpg', np.array(out, dtype=np.uint8))