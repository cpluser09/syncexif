from backup_picture import backup_pictures
from sync_pictures import sync_pictures

#FOLDER_SOURCE = "/Volumes/FUJI"
FOLDER_SOURCE = "/Users/junlin/Downloads"
FOLDER_BACKUP = "/Users/junlin/myPhoto/Photography18/xxx"

FOLDER_SYNC_SOURCE = "/Users/junlin/myPhoto"
#FOLDER_SYNC_DESTINATION = "/Volumes/myPhoto"
FOLDER_SYNC_DESTINATION = "/Users/junlin/myPhoto2"

FILE_FILTERS = [".jpg", ".JPG", ".jpeg", ".JPEG", ".raf", ".RAF", ".png", ".PNG", ".PSD", ".psd"]


if __name__ == '__main__':
    backup_pictures(FOLDER_SOURCE, FOLDER_BACKUP, FILE_FILTERS)
    sync_pictures(FOLDER_SYNC_SOURCE, FOLDER_SYNC_DESTINATION, FILE_FILTERS)