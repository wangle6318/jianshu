from PIL import Image
import re, os
import datetime as dt

#URL = "http://ws1.sinaimg.cn/mw600/6cb9d703gy1g4ff31434ej20o81eokan.jpg"
# URL = "https://ss2.baidu.com/6ONYsjip0QIZ8tyhnq/it/u=1774778828,2365730237&fm=173&app=25&f=JPEG"
# SAVE_PATH = os.path.join(settings.MEDIA_ROOT, 'haveimg\\')
# TEXT_BODY = Article.objects.get(id=5).body


def get_img_url(text):
    # pattern = r'<img src="([^"]+)"'
    #不包含表情包图
    # pattern = r'<img src="((?!http://img.baidu.com/hi/)\S+)"'
    pattern = r'src="((?!http://img.baidu.com/hi/)\S+)"'
    reg = re.findall(pattern, text)
    return reg


def save_img(url, save_path):
    img_suffixes = ['jpg', 'jpeg', 'png', 'gif', 'jfif', 'bmp']
    from uuid import uuid1
    img_suffix = url.split(".")[-1]
    if img_suffix.lower() not in img_suffixes:
        img_suffix = 'jpg'
    file_name = str(uuid1()) + "." + img_suffix
    from urllib.request import urlretrieve
    path_file = save_path + file_name
    try:
        urlretrieve(url, path_file)
    except Exception:
        return None
    return path_file


def crop_img(scale=1.0, open_path='', save_path=''):
    if open_path:
        img = Image.open(open_path)
    else:
        return None
    r_width, r_height = img.size
    r_scale = float(r_height / r_width)
    v_scale = float(scale)
    if r_scale > v_scale:
        width = r_width
        height = int(width * v_scale)
        x = 0
        y = (r_height - height) / 3
    else:
        height = r_height
        width = int(height * v_scale)
        x = (r_width - width) / 2
        y = 0
    box = (x, y, x + width, y + height)
    new_img = img.crop(box)
    if save_path:
        new_img.save(save_path)
        return save_path
    else:
        new_img.save(open_path)
        print("已剪切")
        return open_path





