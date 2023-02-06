from exif import Image
from typing import Dict
import json

import os
image_path = 'C:/Users/G.Tishchenko/Desktop/screenCap/'
folder_screens = os.listdir(path=image_path)


#
def read_screen_comment(screen_shot_path):
    image = Image(screen_shot_path)
    if image.has_exif:
        try:
            return json.loads(image.user_comment) # xp_comment
        except:
            print(f"В {screen_shot_path} нет user_comment\n", image.list_all())
    else:
        return False

# print(folder_screens)
for jpg_screen in folder_screens:
    print(jpg_screen)
    a = read_screen_comment(image_path + jpg_screen)
    print(type(a), a)
