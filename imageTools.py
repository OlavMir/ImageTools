from wrappers import try_func
from exif_tools import ImageInfo
from dbapi import DBConnection
from exif_tools import get_images_info, print_image_info, set_gpstag_to_image, get_info_from_image
from os_tools import get_files_list
import yaml

@try_func
def update_gps_tags(tagged_images_dir:str='', non_tagged_images_dir:str=''):
    """
    Update gps tags in folder nontaged_images_folder in config.
    1. Update db
    2. For every image in folder check time in db, if exist - write gps tag to image
    
    """
    if not tagged_images_dir:
        with open("config.yaml", 'r') as ymlfile:
            config = yaml.safe_load(ymlfile)
        tagged_images_dir = config.get('taged_images_folder')
    if not tagged_images_dir:
        raise Exception("Empty taged_images_folder")
    tagged_images_path_list = get_files_list(tagged_images_dir, ('.jpg', '.jpeg'))
    print(len(tagged_images_path_list))
    images_info = get_images_info(tagged_images_path_list)
    dbConn = DBConnection()
    update_db(images_info)
    if not non_tagged_images_dir:
        with open("config.yaml", 'r') as ymlfile:
            config = yaml.safe_load(ymlfile)
        non_tagged_images_dir = config.get('nontaged_images_folder')
    if not non_tagged_images_dir:
        raise Exception("Empty non_tagged_images_dir")
    non_tagged_images = get_files_list(non_tagged_images_dir, ('.jpg', '.jpeg'))
    print(f'non_tagged_images {len(non_tagged_images)}')
    process_images(dbConn, non_tagged_images)


def update_db(images_info: list[ImageInfo]):
    """
    Update db from folder taged_images_folder in config
    1. Connect to db
    2. Get data from db
    3. Get images information from folder taged_images_folder
    4. Check, are all images from folder in db? If not - insert into db
    """
    dbConn = DBConnection()
    dbConn.connect_to_db()
    print(dbConn.get_db_data())
    db_images_names = dbConn.get_db_images_names()
    inserted = 0
    for image_info in images_info:
        if image_info.name not in db_images_names:
            dbConn.insert_in_db(image_info)
            inserted += 1
    print(f'in db was {len(db_images_names)} images, added {inserted}')


def process_images(dbConn: DBConnection, non_tagged_images: list[str]):
    """
    Try to found gps tag in db for images from non_tagged_images list paths
    """    
    founded = 0
    for img in non_tagged_images:
        try:
            imgInfo = get_info_from_image(img)
            if imgInfo:
                tag_info = dbConn.get_from_db_gpstag_in_delta(imgInfo.time, 20)
                if tag_info:
                    print(f'\tfor {img} found {len(tag_info)} tag(s). For example: {tag_info[0]}')
                    # set_gpstag_to_image()
                    founded += 1
        except Exception as err:
            print(f"Error getting info from image {img}: {err}")
    print(f"Images in directory: {len(non_tagged_images)}. Found Gps tag for {founded}")
    