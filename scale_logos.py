from PIL import Image, ImageGrab, ImageOps
from os import walk


dir_path = r'logo_new'
filenames = list(walk(dir_path))[0][2]
print(filenames)

for i in range(len(filenames)):
    img_orig = Image.open(f'logo_new/{filenames[i]}')
    # впишем скриншот в квадрат 1000x1000 пикселей
    # img = ImageOps.contain(img_orig, (900, 900), method=Image.LANCZOS)
    img = ImageOps.pad(img_orig, (840, 840), color='#ffffff', method=Image.LANCZOS, centering=(0.5, 0.5))

    img.save(f'logo_new_scaled/{filenames[i]}')
