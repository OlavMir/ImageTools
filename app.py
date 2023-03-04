from dbapi import DBConnection
from exif_tools import get_images_info, print_image_info


dbConn = DBConnection()
dbConn.connect_to_db()
dbData = dbConn.get_db_data()
# db_images_names = dbConn.get_db_images_names()
# print(f'in db {len(db_images_names)} images')
images_info = get_images_info()

# for image_info in images_info:
#     if image_info.name not in db_images_names:
#         print(f"Insert {image_info.name}")
#         dbConn.insert_in_db(image_info)
