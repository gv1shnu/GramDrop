from instabot import Bot
from PIL import Image
import PIL.Image
import numpy as np
import os
import shutil
import tempfile
import string
import random
import glob
import time
from scipy.optimize import minimize_scalar
from colorama import init, Fore, Style


def cprint(s, color=Fore.YELLOW, brightness=Style.BRIGHT, **kwargs):
    """Utility function wrapping the regular `print()` function
    but with colors and brightness"""
    print(f"{brightness}{color}{s}{Style.RESET_ALL}", **kwargs)


def _entropy(data):
    """Calculate the entropy of an image"""
    hist = np.array(PIL.Image.fromarray(data).histogram())
    hist = hist / hist.sum()
    hist = hist[hist != 0]
    return -np.sum(hist * np.log2(hist))


def crop(x, y, data, w, h):
    """Crop an image based on the provided coordinates and dimensions"""
    x = int(x)
    y = int(y)
    return data[y: y + h, x: x + w]


def crop_maximize_entropy(img, min_ratio=4 / 5, max_ratio=90 / 47):
    """Crop an image based on the provided coordinates and dimensions"""
    w, h = img.size
    data = np.array(img)
    ratio = w / h
    if ratio > max_ratio:  # Too wide
        w_max = int(max_ratio * h)

        def _crop(_x):
            return crop(_x, y=0, data=data, w=w_max, h=h)

        xy_max = w - w_max
    else:  # Too narrow
        h_max = int(w / min_ratio)

        def _crop(y):
            return crop(x=0, y=y, data=data, w=w, h=h_max)

        xy_max = h - h_max

    to_minimize = lambda xy: -_entropy(_crop(xy))
    x = minimize_scalar(to_minimize, bounds=(0, xy_max), method="bounded").x
    return PIL.Image.fromarray(_crop(x))


def strip_exif(img):
    """Strip EXIF data from the photo to avoid a 500 error."""
    data = list(img.getdata())
    image_without_exif = PIL.Image.new(img.mode, img.size)
    image_without_exif.putdata(data)
    return image_without_exif


def correct_ratio(photo):
    """Check if the aspect ratio of the photo matches Instagram's compatible aspect ratio"""
    from instabot.api.api_photo import compatible_aspect_ratio, get_image_size
    return compatible_aspect_ratio(get_image_size(photo))


def prepare_and_fix_photo(photo):
    """Prepare and fix the photo by stripping EXIF data, cropping if necessary, and saving as .jpg"""
    N = 8
    with open(photo, "rb") as f:
        img = PIL.Image.open(f)
        img = strip_exif(img)
        if not correct_ratio(photo):
            img = crop_maximize_entropy(img)
        res = ''.join(random.choices(string.ascii_lowercase, k=N))
        photo = os.path.join(tempfile.gettempdir(), res + ".jpg")
        img.save(photo)
    return photo


def tojpg(filepath):
    """Convert images in the specified folder to .jpg format"""

    extensions = ['.jpeg', '.png']
    for ext in extensions:
        files = glob.glob(filepath + '\*' + ext)
        # Rename
        for file in files:
            im = Image.open(file)
            rgb_im = im.convert('RGB')
            rgb_im.save(file.replace(ext[1:], "jpg"), quality=95)
        # Delete duplicates
        for f in files:
            os.remove(f)


def remove_config():
    """Remove existing configuration folder"""
    if os.path.isdir("./config"):
        shutil.rmtree("./config")
    else:
        pass


def upload(img, caption):
    """Upload the image to Instagram with the provided caption"""
    try:
        bot.upload_photo(prepare_and_fix_photo(img), caption)
    except Exception as e:
        print("Exception: {}".format(str(e)))
        print("Failed to upload {}\n".format(img))


def main():
    print("Trying to login...")
    try:
        bot.login(username=username, password=password)
        cprint("Login successful.")
    except KeyError:
        cprint("Incorrect credentials")
        exit(1)

    start_time = time.time()
    cprint("Converting all images in the folder to .jpg extension.")
    tojpg(path)
    cprint("All images converted to JPG format.")

    img_files = glob.glob(path + '\*.jpg')
    cprint("Uploading {} JPG files".format(len(img_files)))

    for i, link in enumerate(img_files):
        upload(str(link), "Uploaded by Python")
        cprint("{}/{}".format(i + 1, len(img_files)))

    last_time = time.time()
    cprint("Time elapsed: {} minutes".format(round((last_time - start_time) / 60, 1)))

    remove_config()
    cprint("Check your IG")


if __name__ == '__main__':
    init()
    print("Colorama initiated")

    remove_config()
    print("Existing config cleared")

    path = input("Enter images folder path: ")
    username = input("Enter instagram username: ")
    password = input("Enter instagram password: ")

    bot = Bot()
    print("Bot initiated")

    main()
