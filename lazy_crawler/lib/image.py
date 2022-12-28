import os
import pathlib
import shutil
from io import BytesIO
import gc
import requests
from PIL import Image

def process_image(image_url, image_name):
    try:
        if image_url == '':
            return ''
        base_image_path = str(pathlib.Path().resolve())

        user_path = base_image_path + "/images" + '/'

        # image_name = image_url.split('?')[0].split('/')[-1]

        image_path = user_path + image_name

        pathlib.Path(user_path).mkdir(parents=True, exist_ok=True)
        # del image_name
        del user_path

        image_formats = ("image/png", "image/jpeg", "image/jpg")

        if not os.path.isfile(image_path):
            r = requests.get(image_url, stream=True)
            if r.headers["content-type"] in image_formats:  # if  The given data is image then
                # 1. check if it is already downloaded.if no, download
                # 2.  Get image dimension
                # 3. return (image_urls seperated by pipe,image_local_path_seperated_by_pipe,image dimension seperated by path)
                with open(image_path, 'wb') as out_file:
                    shutil.copyfileobj(r.raw, out_file)
                    del out_file

                im = Image.open(image_path)

                del r
                return image_path
            else:
                del r
                return ''
        else:
            print('Already downloaded', image_path)
            im = Image.open(image_path)
            
        
            if im != '':
                size = im.size
                del im
                gc.collect()
                dimension = '*'.join([str(size[0]), str(size[1])])
                return dimension, '/' + image_name, image_url
            
            del im
            gc.collect()

            return image_path
    except:
        return ''

