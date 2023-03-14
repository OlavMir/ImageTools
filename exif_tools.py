
from exif import Image
import pathlib
import yaml
from datetime import datetime

class ImageInfo:
    def __init__(self, name, time, latitude, latitude_ref, longitude, longitude_ref) -> None:
        self.name = name
        self.time = time
        self.timestamp = datetime.strptime(time, '%Y:%m:%d %H:%M:%S')
        self.gps_tag = GpsTag(latitude, latitude_ref, longitude, longitude_ref)

class GpsTag:
    def __init__(self, latitude, latitude_ref, longitude, longitude_ref) -> None:
        self.latitude = latitude
        self.latitude_ref = latitude_ref
        self.longitude = longitude
        self.longitude_ref = longitude_ref
        if self.latitude and self.latitude_ref and self.longitude and self.longitude_ref:
            self.d_latitude = dms_coordinates_to_dd_coordinates(self.latitude, self.latitude_ref)
            self.d_longitude = dms_coordinates_to_dd_coordinates(self.longitude, self.longitude_ref)
        else:
            self.d_latitude = None
            self.d_longitude = None
    

def get_images_info(image_path_list: list[str]) -> list[ImageInfo]:
    """
    Get images information from list images 
    """
    res = []
    for image_path in image_path_list: 
        try:
            imgInfo = get_info_from_image(image_path)
            if imgInfo:
                res.append(imgInfo)
        except Exception as err:
            print(f"Error getting info from image {image_path}: {err}")
    print(f"Finish. {len(image_path_list)} read, {len(res)} has information")
    return res        
    

def get_info_from_image(img, _print=False) -> ImageInfo:
    """
    Get information from exif.
    return: instanse ImageInfo
    """
    imginfo = None
    with open(img, "rb") as imgps:
        image = Image(imgps)
    if image.has_exif:
        if _print: print_image_info(image=image)
        imginfo = ImageInfo(
            name=str(img).split('\\')[-1].split('.')[0], 
            time=f"{image.datetime_original}",
            latitude= image.get('gps_latitude', None),
            latitude_ref=image.get('gps_latitude_ref', None),
            longitude=image.get('gps_longitude', None),
            longitude_ref=image.get('gps_longitude_ref', None)
        )
    else:
        print(f"\tIn image {img} no data in EXIF.")
    return imginfo

def set_gpstag_to_image(img, _gps_tag: GpsTag) -> None:
    """
    Set gps tag into exif
    """
    with open(img, "rb") as imgps:
        image = Image(imgps)
    image.gps_latitude = _gps_tag.latitude
    image.gps_latitude_ref = _gps_tag.latitude_ref
    image.gps_longitude = _gps_tag.longitude
    image.gps_longitude_ref = _gps_tag.longitude_ref
    _imar = img.split('.')
    new_jpg = f"{_imar[0]}_gps.{_imar[1]}"

    with open(new_jpg, 'wb') as updated_image:
        updated_image.write(image.get_file())
    

def print_image_info(image: Image) -> None:
    """
    Print info from exif
    """
    if image.has_exif:
        print(f"\tcontains EXIF (version {image.exif_version}) information.")
        print(f"\t---------------------")
        print(f"\tLens make: {image.get('lens_make', 'Unknown')}")
        print(f"\tLens model: {image.get('lens_model', 'Unknown')}")
        print(f"\tLens specification: {image.get('lens_specification', 'Unknown')}")
        print(f"\t{image.datetime_original}.{image.subsec_time_original} {image.get('offset_time', '')}\n")
        print(f"\tLatitude: {image.gps_latitude} {image.gps_latitude_ref}")
        print(f"\tLongitude: {image.gps_longitude} {image.gps_longitude_ref}\n")
        print(f'\t type lat {type(image.gps_latitude)}')
        strlat = str(image.gps_latitude)
        print(f'\t str lat {strlat}')
        print(f"\tLatitude (DMS): {format_dms_coordinates(image.gps_latitude)} {image.gps_latitude_ref}")
        print(f"\tLongitude (DMS): {format_dms_coordinates(image.gps_longitude)} {image.gps_longitude_ref}\n")
        print(f"\tLatitude (DD): {dms_coordinates_to_dd_coordinates(image.gps_latitude, image.gps_latitude_ref)}")
        print(f"\tLongitude (DD): {dms_coordinates_to_dd_coordinates(image.gps_longitude, image.gps_longitude_ref)}\n")
        print(f"\tOS version: {image.get('software', 'Unknown')}\n")     
    else:
        print(f"\tno data in EXIF.")
    

def set_info_to_image():
    pass


def draw_map_for_location(latitude, latitude_ref, longitude, longitude_ref):
    """
    Open geotag on google maps
    """
    import webbrowser
    
    decimal_latitude = dms_coordinates_to_dd_coordinates(latitude, latitude_ref)
    decimal_longitude = dms_coordinates_to_dd_coordinates(longitude, longitude_ref)
    url = f"https://www.google.com/maps?q={decimal_latitude},{decimal_longitude}"
    webbrowser.open_new_tab(url)

def dms_coordinates_to_dd_coordinates(coordinates, coordinates_ref):
    """
    Convert (gg, mm, ss) ref to decimal coordinates
    """
    decimal_degrees = coordinates[0] + coordinates[1] / 60 + coordinates[2] / 3600
    
    if coordinates_ref == "S" or coordinates_ref == "W":
        decimal_degrees = -decimal_degrees
    
    return decimal_degrees

def format_dms_coordinates(coordinates: tuple) -> str:
    """
    return formated string from gms coordinates
    """
    return f"{coordinates[0]}° {coordinates[1]}\' {coordinates[2]}\""

