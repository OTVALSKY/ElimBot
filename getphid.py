# getphid.py
# get HD profile picture by user id, save it, overlay it, save again, return overlayed file into main
# if user has no profile pictures, or they are hidden, generate image with black background, containg user initials,
# then downscale to 320p and return file into main 
import asyncio
import os
import config as cfg
from aiogram import Bot
from getimg import getimg

bot=Bot(token=cfg.TOKEN)
script_directory = os.path.dirname(os.path.abspath(__file__))
dest = os.path.join(script_directory, 'getimg/img/photo.jpg') #folder to save image downloaded
user_name=''

async def get_initials(username):
    words = username.split()
    initials = [word[0].upper() for word in words]
    return ' '.join(initials)

class PhotoSize:
   async def __init__(self, file_id, file_unique_id, width, height, file_size):
        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.width = width
        self.height = height
        self.file_size = file_size

async def find_max_pfp_size_by_uid(uid, uName):
    list=await bot.get_user_profile_photos(user_id=uid, offset=0,limit=1)
    nested_list = list.photos
    # Initialize variables to track the max file_size and corresponding file_id
    max_file_size = float('-inf')  # Set to negative infinity initially
    max_file_id = None
    if max_file_id is None:
       output_path = await getimg.genImageNoUser(await get_initials(uName))
       return output_path
    else:
        for sublist in nested_list:
            for photo in sublist:
                if photo.file_size > max_file_size:
                    max_file_size = photo.file_size
                    max_file_id = photo.file_id
        file=await bot.get_file(file_id=max_file_id)
        await bot.download_file(file_path=file.file_path, destination=dest) #file downloaded
        output_path = await getimg.genImageForUser(dest)
        return output_path
     
