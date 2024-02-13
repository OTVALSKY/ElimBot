#init
from pathlib import Path
from db import db
from PIL import Image, ImageDraw, ImageFont
script_directory = Path(__file__).parent
output_path = overlay = script_directory /"img"/"out.jpg"
alpha=1.0
box=(0,0)
print(__name__)
print(__package__)

#init
# create an image, regardless user has avatar or not
async def genImageNoUser(Initials, cid):
    overlay = await db.getOV_path(cid)
    bSize = (320,320)
    img = Image.new("RGB", bSize, (0, 0, 0))
    fnt = ImageFont.truetype(font="arial.ttf", size=150, index=0, encoding="UTF-8")
    draw = ImageDraw.Draw(img)
    x, y, w, h = draw.textbbox((0,0), text=Initials, font=fnt, align="center", font_size=150)
    xx = (320 - w) // 2 #calc coords to center image
    yy = (320 - h) // 2 #calc coords to center text on image
    d = ImageDraw.Draw(img)
    # draw multiline text
    d.multiline_text((xx, yy), Initials, font=fnt, fill=(255, 255, 255), align="center")
    #img.save(output_path)
    res  = Image.Resampling.NEAREST
    bg_img = img
    fg_img = Image.open(overlay)
    (width, height) = (fg_img.width // 2, fg_img.height // 2)
    fg_img = fg_img.resize((width, height))
    fg_img_trans = Image.new("RGBA",fg_img.size)
    fg_img_trans = Image.blend(fg_img_trans,fg_img,alpha)
    bg_img.paste(fg_img_trans,(0,0),fg_img_trans)
    p=bg_img
    p.save(output_path)
    return output_path

async def genImageForUser(dest, cid):
    overlay = await db.getOV_path(cid)
    bg_img = Image.open(dest)
    fg_img = Image.open(overlay)
    fg_img_trans = Image.new("RGBA",fg_img.size)
    fg_img_trans = Image.blend(fg_img_trans,fg_img,alpha)
    bg_img.paste(fg_img_trans,box,fg_img_trans)
    p=bg_img
    p.save(output_path)
    return output_path
