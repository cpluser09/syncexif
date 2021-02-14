import sys
import os
from backup_picture import backup_pictures
from sync_pictures import sync_pictures
from sync_exif import sync_exif
sys.path.append("../photosummary")
from photo_summary import process

JUST_SYNC_FILE=0

FOLDER_SOURCE = "/Volumes/FUJI"
#FOLDER_SOURCE = "/Volumes/RICOH_GR"
FOLDER_BACKUP = "/Volumes/HIKVISION/myPhoto/Photography21/20210214_上海动物园"


FOLDER_SYNC_SOURCE = "/Volumes/HIKVISION/myPhoto"
#FOLDER_SYNC_SOURCE = "/Users/junlin/myPhoto"
FOLDER_SYNC_DESTINATION = "/Volumes/myPhoto"

FILE_FILTERS = [".jpg", ".JPG", ".jpeg", ".JPEG", ".raf", ".RAF", ".png", ".PNG", ".PSD", ".psd", ".mp4", ".MP4", ".mov", ".MOV", ".dng", ".DNG", ".tif", ".TIF"]

def generate_photo_summary(source_folder):
    os.chdir("../photosummary")
    process(source_folder)

if __name__ == '__main__':
    if JUST_SYNC_FILE == 0:
        backup_pictures(FOLDER_SOURCE, FOLDER_BACKUP, FILE_FILTERS)
        sync_exif(FOLDER_BACKUP)
        #generate_photo_summary(FOLDER_BACKUP)
    sync_pictures(FOLDER_SYNC_SOURCE, FOLDER_SYNC_DESTINATION, FILE_FILTERS)
