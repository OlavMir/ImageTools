from exif_tools import ImageInfo
from datetime import datetime, timedelta
from os.path import isfile
import sqlite3    

class DBConnection(object):
    __connection = None
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DBConnection, cls).__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        if not self.__connection:
            self.connect_to_db()

    def __del__(self):
        if self.__connection:
            self.__connection.close() 

    def connect_to_db(self) -> None:
        if self.__connection:
            return
        if isfile('gps_tags.db'):
            self.__connection = sqlite3.connect('gps_tags.db')
        else:
            self.__connection = sqlite3.connect('gps_tags.db')
            cursor = self.__connection.cursor()
            res = cursor.execute('''CREATE TABLE IF NOT EXISTS GPSTAGS
                        (name TEXT, time TEXT, timestamp TIMESTAMP, latitude Decimal(8,6), longitude Decimal(9,6))''')
            res = cursor.fetchall()
            self.__connection.commit()    

    def insert_in_db(self, image_info: ImageInfo) -> None:
        cursor = self.__connection.cursor()
        if image_info.gps_tag.d_latitude and image_info.gps_tag.d_longitude:
            cursor.execute(f"""insert into GPSTAGS values ('{image_info.name}', \
                                                        '{image_info.time}', '{image_info.timestamp}', '{image_info.gps_tag.d_latitude}', \
                                                        '{image_info.gps_tag.d_longitude}');""") 
            self.__connection.commit()  
        return

    def get_db_data(self) -> list:
        res = []
        cursor = self.__connection.cursor()
        cursor.execute('''SELECT * from GPSTAGS''')
        res = cursor.fetchall()
        print(f'DB data: {res}')
        for line in res:
            print(line)
        return res

    def get_db_images_names(self) -> list[str]:
        cursor = self.__connection.cursor()
        cursor.execute('''SELECT * from GPSTAGS''')
        res = cursor.fetchall()
        return [info[0] for info in res]

    def get_from_db_gpstag_in_delta(self, time: str, delta_minutes: int):
        
        try:
            _time = datetime.strptime(time, '%Y:%m:%d %H:%M:%S')
        except Exception as err:
            raise err
        # print(f'Get gps tag from db for time {time} between {_time - timedelta(minutes=delta_minutes)} and {_time + timedelta(minutes=delta_minutes)}')
        cursor = self.__connection.cursor()
        cursor.execute(f"""select * from GPSTAGS where timestamp between '{_time - timedelta(minutes=delta_minutes)}' and '{_time + timedelta(minutes=delta_minutes)}' """)
        res = cursor.fetchall()
        return res
        
        