
from exif import Image
import pathlib
import yaml

class ImageInfo:
    def __init__(self, name, time, lat, lon) -> None:
        self.name = name
        self.time = time
        self.latitude = lat
        self.longitude = lon
        # self.lon_ref = lon_ref
    

def get_images_info() -> list[ImageInfo]:
    print('Get images info')
    res = []
    with open("config.yaml", 'r') as ymlfile:
        config = yaml.safe_load(ymlfile)
    imgDir = pathlib.Path(config.get('taged_images_folder'))
    imgs = list(imgDir.rglob("*.jpg"))
    for img in imgs:
        imgInfo = get_info_from_image(img)
        if imgInfo:
            res.append(imgInfo)
    print(f"Finish. {len(imgs)} read, {len(res)} has information")
    return res        
    

def get_info_from_image(img) -> ImageInfo:
    imginfo = None
    with open(img, "rb") as imgps:
        image = Image(imgps)
    if image.has_exif:
        print_image_info(image=image)
        imginfo = ImageInfo(
            name=str(img).split('\\')[-1].split('.')[0], 
            time=f"{image.datetime_original}.{image.subsec_time_original} {image.get('offset_time', '')}",
            lat=dms_coordinates_to_dd_coordinates(image.gps_latitude, image.gps_latitude_ref),
            # lat_ref=image.gps_latitude_ref,
            lon=dms_coordinates_to_dd_coordinates(image.gps_longitude, image.gps_longitude_ref)
            # lon_ref=image.gps_longitude_ref
        )
    else:
        print(f"\tdoes not contain any EXIF information.")
    return imginfo

def print_image_info(image: Image) -> None:
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
        # print(f"\tLatitude (DMS): {format_dms_coordinates(image.gps_latitude)} {image.gps_latitude_ref}")
        # print(f"\tLongitude (DMS): {format_dms_coordinates(image.gps_longitude)} {image.gps_longitude_ref}\n")
        print(f"\tLatitude (DD): {dms_coordinates_to_dd_coordinates(image.gps_latitude, image.gps_latitude_ref)}")
        print(f"\tLongitude (DD): {dms_coordinates_to_dd_coordinates(image.gps_longitude, image.gps_longitude_ref)}\n")
        # print(f"\tOS version: {image.get('software', 'Unknown')}\n")
        # draw_map_for_location(
        #     image.gps_latitude, 
        #     image.gps_latitude_ref, 
        #     image.gps_longitude,
        #     image.gps_longitude_ref
        # )       
    else:
        print(f"\tdoes not contain any EXIF information.")
    

def set_info_to_image():
    pass


def draw_map_for_location(latitude, latitude_ref, longitude, longitude_ref):
    import webbrowser
    
    decimal_latitude = dms_coordinates_to_dd_coordinates(latitude, latitude_ref)
    decimal_longitude = dms_coordinates_to_dd_coordinates(longitude, longitude_ref)
    url = f"https://www.google.com/maps?q={decimal_latitude},{decimal_longitude}"
    webbrowser.open_new_tab(url)

def dms_coordinates_to_dd_coordinates(coordinates, coordinates_ref):
    decimal_degrees = coordinates[0] + coordinates[1] / 60 + coordinates[2] / 3600
    
    if coordinates_ref == "S" or coordinates_ref == "W":
        decimal_degrees = -decimal_degrees
    
    return decimal_degrees

def format_dms_coordinates(coordinates):
    return f"{coordinates[0]}° {coordinates[1]}\' {coordinates[2]}\""