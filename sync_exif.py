#import pexif
import sys
import math
import piexif
import piexif.helper
from PIL import Image 

def dump_exif():
    #file_name = "/Users/junlin/test/gps/IMG_3777.JPG"
    #file_name = "/Users/junlin/test/gps/IMG_5180.JPG"
    file_name = "/Users/junlin/test/gps/no_gps.jpg"
    exif_dict = piexif.load(file_name)
    for ifd in ("0th", "Exif", "GPS", "1st"):
        print("===================", ifd, "=====================")
        for tag in exif_dict[ifd]:
            print(piexif.TAGS[ifd][tag]["name"], exif_dict[ifd][tag])

# 转换纬度 DMS (degree minute second)
def convert_lat_to_dms(latitude):
    latitude = math.fabs(latitude)
    degree = math.floor(latitude)
    minute = math.floor((latitude - degree)*60)
    second = float(latitude*3600 - degree*3600 - minute*60)
    return ((degree, 1), (minute, 1), (math.floor(second*1000000), 1000000))

# 转换经度
def convert_log_to_dms(longitude):
    longitude = math.fabs(longitude)
    degree = math.floor(longitude)
    minute = math.floor((longitude - degree)*60)
    second = float(longitude*3600 - degree*3600 - minute*60)
    return ((degree, 1), (minute, 1), (math.floor(second*1000000), 1000000))

def create_gps_ifd(longitude, latitude):
    ifd_list = []
    ifd_list.append("%d: (2, 0, 0, 0)" % piexif.GPSIFD.GPSVersionID)

    EW = "E"
    if(longitude < 0.0):
        EW = "W"
    ifd_list.append("%d: %s" % (piexif.GPSIFD.GPSLongitudeRef, EW))
    ifd_list.append( ("%d: %s" % (piexif.GPSIFD.GPSLongitude, convert_log_to_dms(longitude))) )

    SN = "N"
    if(latitude < 0.0):
        SN = "S"
    ifd_list.append("%d: %s" % (piexif.GPSIFD.GPSLatitudeRef, SN))
    ifd_list.append( ("%d: %s" % (piexif.GPSIFD.GPSLatitude, convert_lat_to_dms(latitude))) )

    # 
    gps_ifd = { piexif.GPSIFD.GPSVersionID: (2, 0, 0, 0),  # BYTE, count 4
        piexif.GPSIFD.GPSLongitudeRef: EW,
        piexif.GPSIFD.GPSLongitude: convert_log_to_dms(longitude),
        piexif.GPSIFD.GPSLatitudeRef: SN,
        piexif.GPSIFD.GPSLatitude: convert_lat_to_dms(latitude)
    }
    return gps_ifd

def process(source_file):
    gps_ifd = create_gps_ifd(121.30265, 31.150299999999998)
    print("---->>", gps_ifd)
    exif_dict = {"GPS":gps_ifd}
    exif_raw = piexif.dump(exif_dict)
    piexif.insert(exif_raw, source_file)
    print("Done.")

if __name__ == '__main__':
    dump_exif()
    file_name = "/Users/junlin/test/gps/IMG_5180.JPG"
    file_name = "/Users/junlin/test/gps/no_gps.JPG"
    process(file_name)
    sys.exit()