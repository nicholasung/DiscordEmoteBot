from PIL import Image, ImageOps
from PIL import *
import io

async def compress(b_img):
    # MAIN FUNCTION THAT CALLS HELPERS THAT WILL CONVERT BYTE TO PIL IMG, COMPRESS AND THEN RETURN THE COMPRESSED AS A BYTES OBJECT AGAIN
    p_img = Image.open(io.BytesIO(b_img))
    # compress image 128*128 (integer scale for discord) 
    emote_resolution = (128, 128)
    comp_img = ImageOps.fit(p_img, emote_resolution)
    # convert comp_img to byte string
    comp_b_img = io.BytesIO()
    comp_img.save(comp_b_img, format='PNG')
    return comp_b_img.getvalue()

async def clean(b_img):
    # function called after compress to delete the original and compressed files based on a call from main
    return None