from PIL import Image
import glob, os

size = 128, 128

for infile in glob.glob("./img/*.JPEG"):
    file, ext = os.path.splitext(infile)
    im = Image.open(infile).convert('L')
    im.thumbnail(size, Image.ANTIALIAS)
    # im.save(file + ".png")

    im.save(file + ".jpg", "JPEG")