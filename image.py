import re
import os
from PIL import Image, ImageFilter
from wand.image import Image as magicImage
from wand.api import library


def resizeAspect(img_path, height=None, width=None):
    """Resize image while preserving aspect ratio of original image. Dimension format is width x height"""

    print("before load: ", os.getcwd())

    load_img = Image.open(img_path)

    print("after load: ", os.getcwd())

    if height is None and width is None:
        return img_path

    (w, h) = load_img.size[:2]

    if height is not None:
        ratio = height / float(h)
        print("ratio:", ratio)
        # dimension = (int(ratio*w), height)
        dimension = (int(ratio * w), height)
    else:
        ratio = width / float(w)
        print("ratio:", ratio)
        dimension = (width, int(ratio * h))

    os.chdir(os.path.dirname(img_path))

    file_name = re.sub(".png|.jpg|.jpeg", "", os.path.basename(img_path))
    file_name = "_".join(file_name.split())
    file_name = f"{file_name}_resized.jpg"

    print("original image:", w, h)
    print("new image:", dimension)

    return load_img.resize(dimension, resample=Image.BICUBIC), file_name


def formatImg(bg_img, front_img):
    """Format image to set layout"""

    STD_SIZE = (1200, 630)

    file_name = bg_img

    # load needed images into memory
    canvas = Image.new("RGB", (1200, 630), color="white")

    # resize bg_image to double the standard size to 'fill' canvas
    bg_img = resizeAspect(bg_img, width=1200)
    bg_img = bg_img[0].filter(ImageFilter.GaussianBlur(radius=30))
    canvas.paste(bg_img, (0, 0))

    print("before load: ", os.getcwd())

    # resize front image to fit standard image size
    load_front_img = Image.open(front_img)
    # load_front_img = resizeAspect(front_img,height=630)
    load_front_img.thumbnail(STD_SIZE)

    print("after load: ", os.getcwd())

    img_center = canvas.size[0] // 2  # calculate center of canvas
    front_img_center = load_front_img.size[0] // 2  # calculate center of front image
    diff_centers = img_center - front_img_center

    box = (
        diff_centers + 1,
        0,
    )  # set difference above as coordinate to paste into (x-axis)
    canvas.paste(load_front_img, box)

    file_name = re.sub(".png|.jpg|.jpeg", "", file_name)
    file_name = f"{file_name}_superimposed.jpg"
    return canvas, file_name


def get_images(pathtodir):
    """Retrieves image files within a directory"""
    os.chdir(pathtodir)
    images = []
    for root, dirs, files in os.walk(os.getcwd()):
        for file in files:
            if re.search("jpeg|png|jpg|JPG|JPEG|PNG", file):
                images.append(f"{root}\{file}")
    return images


def proc_images(dir_name):

    images = get_images(dir_name)

    for img in images:
        print(img)
        load_img = Image.open(img)
        width, height = load_img.size[0], load_img.size[1]
        ratio = width / height

        if ratio >= 1.3:
            resized = resizeAspect(img, width=1200)
            try:
                resized[0].save(resized[1], optimize=True, quality=60, dpi=(72, 72))
            except:
                continue
        else:
            formatted_img = formatImg(img, img)
            try:
                formatted_img[0].save(
                    formatted_img[1], optimize=True, quality=60, dpi=(72, 72)
                )
            except:
                continue


def compress_image(filename):
    with magicImage(filename=filename) as img:
        library.MagickSetCompressionQuality(img.wand, 75)
        img.format = "jpeg"
        img.save(filename="test/test.jpg")


proc_images("./wdj/")
# proc_images("./panay-news/")
# proc_images("./photos")

# # for testing
# bg_img = "test2.png"
# front_img= "test2.png"
# format_Img(bg_img, front_img)

# for i in get_images(os.getcwd()):
#     print(i)

# image_files = get_images("panay-news")
# for img in image_files:
#     print(img)

# image_path = "C:\\Users\\Patrick Panizales\\Desktop\\pn-auto\\panay-news\\Kris Aquino.jpg"

# #format image test
# format = formatImg(image_path,image_path)
# format[0].save(format[1])

# #resize aspect test
# resized = resizeAspect(image_path,width=1200)
# resized[0].save(resized[1])

# image_path = "C:\\Users\\Patrick Panizales\\Downloads\\entertainment"
# formatImg(image_path, image_path)
