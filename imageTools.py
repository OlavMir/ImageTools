from dbapi import DBConnection
from exif_tools import get_images_info, print_image_info, set_gpstag_to_image

def update_gps_tags():
    """
    Update gps tags in folder nontaged_images_folder in config.
    1. Update db
    2. For every image in folder check time in db, if exist - write gps tag to image
    
    """
    dbConn = DBConnection()
    update_db()
    dbConn.get_from_db_gpstag_in_delta()


def update_db():
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
    print(f'in db {len(db_images_names)} images')
    images_info = get_images_info()    

    for image_info in images_info:
        if image_info.name not in db_images_names:
            print(f"Insert {image_info.name}")
            dbConn.insert_in_db(image_info)
        else:
            print(f"{image_info.name} already in db")