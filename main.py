from PIL import Image
from pathlib import Path
from os.path import exists
from os import strerror
from errno import ENOENT
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--path", help="Path to the image which should be compromised.")
parser.add_argument("--rate", help="The optimizing rate, default 0.95, which is max 0.01 is the worst", default=0.95)
parser.add_argument("--size", help="Size of the new image as a tuple (x,y), default use is the origin size.", default=(None, None))
ARGS = parser.parse_args()

if __name__ == "__main__":
    path = Path(ARGS.path)
    optimizing_rate = int(ARGS.rate*100)
    im_size = ARGS.size

    #load image
    if exists(str(path)):
        im = Image.open(path)
    else:
        raise FileNotFoundError(
            ENOENT, strerror(ENOENT), str(path))
    #check if valid size is given, if so downsize the image
    if all(im_size):
        if im_size[0] > 0 and im_size[1] > 0:
            im = im.resize(im_size, Image.ANTIALIAS)
    #save the image with new size and quality
    im.save(Path.joinpath(path.parent, f"{path.stem}_compromised{path.suffix}"), optimize=True, quality=optimizing_rate)
    print(f"The Image was compressed and saved to {path.parent} as {path.stem}_compromised{path.suffix}")
