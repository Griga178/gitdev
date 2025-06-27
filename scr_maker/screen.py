import pyautogui
import numpy as np
import cv2
import json
import exif
from typing import Dict

def make_screen(img_name, comment_content: Dict = False):
    image = pyautogui.screenshot(region = (0, 0, 1920, 1080))
    # image = pyautogui.screenshot(region = (0, 0, 2560, 1440))
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    if comment_content:
        """Загружает словарь в метаданные скриншота
        """
        status, image_jpg_coded = cv2.imencode('.jpg', image) # jpg -> numpy ?
        image_jpg_coded_bytes = image_jpg_coded.tobytes() # numpy -> bytes ?
        exif_jpg = exif.Image(image_jpg_coded_bytes) # bytes -> <exif_class> ?

        json_comment = json.dumps(comment_content)
        exif_jpg["user_comment"] = json_comment # <exif_class>.append(comment)
        with open(img_name, 'wb') as new_image_file:
            new_image_file.write(exif_jpg.get_file())
    else:
        cv2.imwrite(img_name, image)
