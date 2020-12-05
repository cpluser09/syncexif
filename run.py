import sys
import os
from backup_picture import backup_pictures
from sync_pictures import sync_pictures
from sync_exif import sync_exif
sys.path.append("../photosummary")
from photo_summary import process

FOLDER_SOURCE = "/Volumes/FUJI"
FOLDER_BACKUP = "/Users/junlin/myPhoto/Photography19/20201205_夏都小镇"

FOLDER_SYNC_SOURCE = "/Users/junlin/myPhoto"
FOLDER_SYNC_DESTINATION = "/Volumes/myPhoto"

FILE_FILTERS = [".jpg", ".JPG", ".jpeg", ".JPEG", ".raf", ".RAF", ".png", ".PNG", ".PSD", ".psd", ".mp4", ".MP4", ".mov", ".MOV"]

def generate_photo_summary(source_folder):
    os.chdir("../photosummary")
    process(source_folder)

if __name__ == '__main__':
    # backup_pictures(FOLDER_SOURCE, FOLDER_BACKUP, FILE_FILTERS)
    # sync_exif(FOLDER_BACKUP)
    # sync_pictures(FOLDER_SYNC_SOURCE, FOLDER_SYNC_DESTINATION, FILE_FILTERS)
    generate_photo_summary(FOLDER_BACKUP)
