from PIL import Image
from PIL import *
import io

async def compress(b_img):
    # MAIN FUNCTION THAT CALLS HELPERS THAT WILL CONVERT BYTE TO PIL IMG, COMPRESS AND THEN RETURN THE COMPRESSED AS A BYTES OBJECT AGAIN
    p_img = Image.open(io.BytesIO(b_img))
    # compress image by some factor and then check if its smaller than 256ks
    # return a bytes
    return None

async def clean(b_img):
    # function called after compress to delete the original and compressed files based on a call from main