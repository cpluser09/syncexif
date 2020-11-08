from backup_picture import backup_pictures
from sync_pictures import sync_pictures
from sync_exif import sync_exif

FOLDER_SOURCE = "/Volumes/FUJI"
FOLDER_BACKUP = "/Users/junlin/myPhoto/new/Photography18/20201107_人民广场"

FOLDER_SYNC_SOURCE = "/Users/junlin/myPhoto"
FOLDER_SYNC_DESTINATION = "/Volumes/myPhoto"

FILE_FILTERS = [".jpg", ".JPG", ".jpeg", ".JPEG", ".raf", ".RAF", ".png", ".PNG", ".PSD", ".psd", ".mp4", ".MP4", ".mov", ".MOV"]


if __name__ == '__main__':
    #backup_pictures(FOLDER_SOURCE, FOLDER_BACKUP, FILE_FILTERS)
    #sync_exif(FOLDER_BACKUP)
    sync_pictures(FOLDER_SYNC_SOURCE, FOLDER_SYNC_DESTINATION, FILE_FILTERS)