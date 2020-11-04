#import pexif
import os
import sys
import math
from os.path import isfile, join
from os import listdir, path, remove
import glob
import json
import requests

import piexif
import piexif.helper
from PIL import Image

GPS_DATABASE_PATH = "/Users/junlin/gps_db"

OPTION_DEBUG = 0

GPS_LOG_FILS = {}

def usage():
	print ("""
usage: add_frame [path_of_picture][-h][-v]

arguments:
    path_of_picture	    path of JPG file
    -d                  enable debug mode
    -h, --help			show this help message and exit
    -v, --version		show version information and exit
""")


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

def search_files(dirname):
    result = []
    filter = [".jpg", ".JPG", ".jpeg", ".JPEG"]
    for filename in os.listdir(dirname):
        apath = os.path.join(dirname, filename)
        ext = os.path.splitext(apath)[1]
        if ext in filter:
            result.append(apath)
    return result

def insert_user_comment(comment, file_name):
    exif_dict = piexif.load(file_name)
    user_comment = piexif.helper.UserComment.dump(u"{\"comment\":\"this is test!\"}")
    exif_dict["Exif"][piexif.ExifIFD.UserComment] = comment
    exif_raw = piexif.dump(exif_dict)
    piexif.insert(exif_raw, file_name)

def get_gps_content(gps_file):
    lines = None
    if gps_file not in GPS_LOG_FILS.keys():
        handle_gps_list = None
        try:
            handle_gps_list = open(gps_file, "rb")
        except FileNotFoundError:
            print ("file is not found.", gps_file)
        except PermissionError:
            print ("don't have permission to access this file.", gps_file)
        if handle_gps_list is  None:
            #print("read file list failed.")
            return None
        lines = handle_gps_list.readlines()
        if len(lines) == 0:
            print("empty file!")
            return None
        # save it 
        GPS_LOG_FILS[gps_file] = lines
    else:
        lines = GPS_LOG_FILS[gps_file]
    return lines

def hms_to_second(hms):
    hour, minute, second = hms.split(":")
    return int(hour) * 3600 + int(minute) * 60 + int(second)

def queryGps(shot_time):
    date, time = shot_time.split(" ")
    gps_file = GPS_DATABASE_PATH + "/" + date.replace(":", "-") + ".txt"
    lines = get_gps_content(gps_file)
    if lines is None:
        return (None, None)
    for line in lines:
        line = line.decode()
        #print(line)
        try:
            gps = json.loads(line)
            if "time" not in gps.keys():
                print("format invalid or no gps info.")
                continue
            gps_date, gps_time = gps["time"].split(" ")
            if gps_date != date:
                continue
            diff = hms_to_second(gps_time) - hms_to_second(time)
            if abs(diff) < 5:                
                print("found shot time: ", shot_time, ", gps time: ", gps_date, gps_time, gps["longitude"], gps["latitude"], gps["thoroughfare"], "diff: ", diff, "secs")
                return (gps["longitude"], gps["latitude"])
                break
        except BaseException:
            continue
        else:
            continue

    return (None, None)

        
def insert_gps(source_file):
    origin_exif = piexif.load(source_file)
    # if "GPS" in origin_exif.keys() and piexif.GPSIFD.GPSLongitude in origin_exif["GPS"].keys():
    #     print("already has GPS in exif.", source_file)
    #     return
    if "Exif" not in origin_exif.keys() or len(origin_exif["Exif"]) == 0:
        print("no exif.", source_file)
        return
    if piexif.ExifIFD.DateTimeOriginal not in origin_exif["Exif"]:
        print("no shot time.", source_file)
        return
    shot_time = origin_exif["Exif"][piexif.ExifIFD.DateTimeOriginal]
    #shot_time = b"2020:08:14 20:05:56"
    longitude, latitude = queryGps(shot_time.decode("utf8"))
    if longitude is None or latitude is None:
        print("not found gps in database.", source_file, shot_time.decode("utf8"))
        return
    gps_ifd = create_gps_ifd(longitude, latitude)
    #print(gps_ifd)
    origin_exif["GPS"] = gps_ifd
    exif_raw = piexif.dump(origin_exif)
    piexif.insert(exif_raw, source_file)
    print("---->>", source_file)

def sync_exif(folder_path):
    files = search_files(folder_path)
    if len(files) == 0:
        print("no file found. %s" % folder_path)
        sys.exit()
    for each_picture in files:
        insert_gps(each_picture)
        if OPTION_DEBUG == 1:
            break
    print("Done.")

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("arguments error!\r\n-h shows usage.")
        #process("/Users/junlin/test/gps")
        sys.exit()
    for arg in sys.argv[1:]:
        if arg == '-v' or arg == "--version":
            print("1.0.0")
            sys.exit()
        elif arg == '-h' or arg == '--help':
            usage()
            sys.exit()
        elif arg == '-d' or arg == '--debug':
            OPTION_DEBUG = 1
    sync_exif(sys.argv[1])