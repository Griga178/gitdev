from exif import Image
#
image_path = 'C:/Users/G.Tishchenko/Desktop/Exif_jpg2.jpg'
image_path2 = 'C:/Users/G.Tishchenko/Desktop/Exif_jpg3.jpg'
# image = Image(image_path)
# #
# # # print(dir(image))
# print(image.has_exif)
# print(image.list_all())
# print(image.user_comment)
# new_coment = 'f'
# my_str_as_bytes = str.encode(new_coment)
# image.user_comment = my_str_as_bytes
# # print(image.user_comment)
# with open(image_path2, 'wb') as new_image_file:
#     new_image_file.write(image.get_file())
# import exif
# import cv2
# import numpy as np
#
# # Create a random 2D array within range [0 255]
# image = (np.random.rand(800, 1200) * 255).astype(np.uint8)
#
# # decode to the appropriate format
# # jpg -> compressed with information loss)
# status, image_jpg_coded = cv2.imencode('.jpg', image)
# print('successful jpg encoding: %s' % status)
# # tif -> no compression, no information loss
# # status, image_tif_coded = cv2.imencode('.jpg', image)
# # print('successful tif encoding: %s' % status)
#
# # to a byte string
# image_jpg_coded_bytes = image_jpg_coded.tobytes()
# # image_tif_coded_bytes = image_tif_coded.tobytes()
#
#
# # using the exif format to add information
# exif_jpg = exif.Image(image_jpg_coded_bytes)
# # exif_tif = exif.Image(image_tif_coded_bytes)
#
# # providing some information
# user_comment = "Hello world! it is my first Exif comment"
# software = "created in python with numpy"
# author = "I am not Rune Monzel"
#
# # adding information to exif files:
# # exif_jpg["software"] = exif_tif["software"] = software
# # exif_jpg["user_comment"] = exif_tif["user_comment"] = user_comment
# exif_jpg["software"] = software
# exif_jpg["author"] = author
# exif_jpg["user_comment"] = user_comment
# exif_jpg["content_price"] = "1000.52"
# exif_jpg["content_name"] = "Телевизор LG 100500 Ultra HD"
# exif_jpg["content_kkn"] = "Телевизор тип 1"
#
# # show existing tags
# print(exif_jpg.list_all())
#
# # save image
# # with open(r'C:/Users/G.Tishchenko/Desktop/random.tif', 'wb') as new_image_file:
# #     new_image_file.write(exif_tif.get_file())
# with open(image_path, 'wb') as new_image_file:
#     new_image_file.write(exif_jpg.get_file())

# def img_add_comment(image, comment):

import json
from datetime import datetime
import exif
import pyautogui
import cv2
import numpy as np

# # Create a random 2D array within range [0 255]
# image = (np.random.rand(800, 1200) * 255).astype(np.uint8)
image = pyautogui.screenshot(region = (0, 0, 1920, 1080))
image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

status, image_jpg_coded = cv2.imencode('.jpg', image) # numpy array
image_jpg_coded_bytes = image_jpg_coded.tobytes()

exif_jpg = exif.Image(image_jpg_coded_bytes)

comment_content = {
    "id": 1,
    "link": "https://www.dns-shop.ru/product/9563422a3edced20/14-noutbuk-realme-book-prime-14-serebristyj/",
    "content_date": datetime.strptime("06.02.2023", "%d.%m.%Y").strftime('%d.%m.%Y'),
    "content_price": 20.05
}
json_comment = json.dumps(comment_content)

exif_jpg["user_comment"] = json_comment

# image_jpg_coded_bytes = np.frombuffer(exif_jpg, dtype=image_jpg_coded.dtype)

image_path2 = 'C:/Users/G.Tishchenko/Desktop/Exif_jpg3.jpg'
# cv2.imwrite(image_path2, image_jpg_coded_bytes)

with open(image_path2, 'wb') as new_image_file:
    new_image_file.write(exif_jpg.get_file())

print(json_comment)
