import os
import sys
import shutil
import time
from progress.bar import Bar

FOLDER_SOURCE = "/Users/junlin/Downloads"
FOLDER_DESTINATION = "/Users/junlin/myPhoto2"
#FOLDER_DESTINATION = "/Volumes/myPhoto"
FILE_FILTERS = [".jpg", ".JPG", ".jpeg", ".JPEG", ".raf", ".RAF", ".png", ".PNG", ".PSD", ".psd"]
global G_TOTAL_SYNC_COUNT

class FancyBar(Bar):
    message = 'Syncing'
    fill = '*'
    suffix = '%(percent).1f%% - %(elapsed)ds [remaining %(remaining)d - total %(max)d]'

def calc_dst_folder(source_file):
    file_with_sub_folder = source_file.replace(FOLDER_SOURCE, "")
    file_full_path = FOLDER_DESTINATION + file_with_sub_folder
    return file_full_path

def sync_file(source_file):
    global G_TOTAL_SYNC_COUNT
    #print("\ntry sync:", source_file)
    dst_file = calc_dst_folder(source_file)
    if os.path.exists(dst_file) == True:
        #print("skip...")
        return False
    dst_folder,_ = os.path.splitext(dst_file)
    dst_folder = dst_folder[0: dst_folder.rfind("/")]
    if os.path.exists(dst_folder) == False:
        os.makedirs(dst_folder)
    shutil.copyfile(source_file, dst_file)
    G_TOTAL_SYNC_COUNT = G_TOTAL_SYNC_COUNT + 1
    #print("sync  to: %12d  %s" % (G_TOTAL_SYNC_COUNT, source_file))
    return True

def search_files(root_name, filter, result):
    #global G_TOTAL_SYNC_COUNT
    for dir_name in os.listdir(root_name):
        file_path = os.path.join(root_name, dir_name)
        if os.path.isdir(file_path):
            search_files(file_path, filter, result)
        else:
            file_name_with_path, ext = os.path.splitext(file_path)
            file_name = file_name_with_path [file_name_with_path.rfind("/")+1: len(file_name_with_path)]
            if ext in filter and file_name[0] != "." and "Trashes" not in file_name_with_path:
                result.append(file_path)
    return result

def sync(files):
    bar = FancyBar()
    bar.max = len(files)
    for n in range(len(files)):
        sync_file(files[n])
        bar.index = n + 1
        bar.update()
    bar.finish()

def let_go():
    folder = FOLDER_SOURCE
    if os.path.exists(folder) == False:
        print("FOLDER_SOURCE not exist.", folder)
        return
    global G_TOTAL_SYNC_COUNT
    G_TOTAL_SYNC_COUNT = 0
    result = []
    result = search_files(folder, FILE_FILTERS, result)
    sync(result)
    print("DONE. total %d source files, %d files synced." % (len(result), G_TOTAL_SYNC_COUNT))

if __name__ == '__main__':
    let_go()