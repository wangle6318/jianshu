from PIL import Image
from django.conf import settings
import os

# open_path = os.path.join(settings.MEDIA_ROOT, 'titleimg\\2019\\8\\d080d794-c25f-11e9-948d-54e1ad5d5a3b.jpg')
#
#
# def crop_img(scale=1.0, open_path='', save_path=''):
#     if open_path:
#         img = Image.open(open_path)
#     else:
#         return None
#     r_width, r_height = img.size
#     r_scale = float(r_height / r_width)
#     v_scale = float(scale)
#     if r_scale > v_scale:
#         width = r_width
#         height = int(width * v_scale)
#         x = 0
#         y = (r_height - height) / 3
#     else:
#         height = r_height
#         width = int(height * v_scale)
#         x = (r_width - width) / 2
#         y = 0
#     box = (x, y, x + width, y + height)
#     new_img = img.crop(box)
#     if save_path:
#         new_img.save(save_path)
#         return save_path
#     else:
#         new_img.save(open_path)
#         return open_path


def checkio(data: list) -> list:
    # Your code here
    # It's main function. Don't remove this function
    # It's used for auto-testing and must return a result for check.
    count = {}
    non_unique = []
    for key in data:
        if key not in count.keys():
            count.setdefault(key, 0)
        count[key] += 1
        if count[key] == 2:
            non_unique.append(key)
    for nu in data:
        if nu not in non_unique:
            data.remove(nu)

    # replace this for solution
    return data

print(checkio([1,2,3,4,5]))