from exif_tools import ImageInfo
from os.path import isfile
import sqlite3    

class DBConnection(object):
    __connection = None
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DBConnection, cls).__new__(cls)
        return cls.instance

    def __del__(self):
        if self.__connection:
            print('Close DB connection')
            self.__connection.close()
        print("DBConnection deleted")   

    def connect_to_db(self) -> None:
        if self.__connection:
            print('connection ok')
            return
        if isfile('gps_tags.db'):
            print(f'DB exist, just connect')
            self.__connection = sqlite3.connect('gps_tags.db')
        else:
            print(f"DB doesn't exist. Create the table.")
            self.__connection = sqlite3.connect('gps_tags.db')
            cursor = self.__connection.cursor()
            res = cursor.execute('''CREATE TABLE IF NOT EXISTS GPSTAGS
                        (name TEXT, time TEXT, timestamp TIMESTAMP, latitude Decimal(8,6), longitude Decimal(9,6))''')
            res = cursor.fetchall()
            print(f"res {res}")
            self.__connection.commit()    

    def insert_in_db(self, image_info: ImageInfo) -> None:
        print("Insert data in db")
        cursor = self.__connection.cursor()
        cursor.execute(f"""insert into GPSTAGS values ('{image_info.name}', \
                                                       '{image_info.time}', '{image_info.timestamp}', '{image_info.gps_tag.d_latitude}', \
                                                       '{image_info.gps_tag.d_longitude}');""") 
        self.__connection.commit()  
        return

    def get_db_data(self) -> list:
        print("Get data from db")
        res = []
        cursor = self.__connection.cursor()
        cursor.execute('''SELECT * from GPSTAGS''')
        res = cursor.fetchall()
        print(f'DB data: {res}')
        for line in res:
            print(line)
        return res

    def get_db_images_names(self) -> list[str]:
        print("Get names from db")
        cursor = self.__connection.cursor()
        cursor.execute('''SELECT * from GPSTAGS''')
        res = cursor.fetchall()
        print(f'DB images names: {res}')
        return [info[0] for info in res]

    def get_from_db_gpstag_in_delta(self, t1, t2):
        print('Get gps tag from db')
        cursor = self.__connection.cursor()
        cursor.execute(f"""select * from GPSTAGS where timestamp between '{t1}' and '{t2}' """)
        res = cursor.fetchall()
        for line in res:
            print(line)
        return res

        
        