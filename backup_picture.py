import os
import sys
import shutil
from progress.bar import Bar

class FancyBar(Bar):
    message = 'Syncing'
    fill = '*'
    suffix = '%(percent).1f%% - %(elapsed)ds [remaining %(remaining)d - total %(max)d]'

def search_files(root_name, filter, result):
    for dir_name in os.listdir(root_name):
        file_path = os.path.join(root_name, dir_name)
        if os.path.isdir(file_path):
            search_files(file_path, filter, result)
        else:
            file_name_with_path, ext = os.path.splitext(file_path)
            file_name = file_name_with_path [file_name_with_path.rfind("/")+1: len(file_name_with_path)]
            if ext in filter and file_name[0] != "." and "Trashes" not in file_path:
                result.append(file_path)
    return result

def backup_pictures(source_folder, dst_folder, file_filter):
    print("begin backup files...")
    folder = source_folder
    if os.path.exists(folder) == False:
        print("source folder not exist. ", folder)
        return
    
    result = []
    result = search_files(folder, file_filter, result)
    sorted(result)
    if len(result) == 0:
        print("No file found.")
        return
    if os.path.exists(dst_folder) == False:
        os.makedirs(dst_folder)

    bar = FancyBar()
    bar.max = len(result)
    total_file_count = 0
    overwrite_count = 0
    for n in range(len(result)):
        each_picture = result[n]
        file_name = each_picture[each_picture.rfind("/")+1: len(each_picture)]
        dst_file_path = dst_folder + "/" + file_name
        if os.path.exists(dst_file_path) == True:
            overwrite_count += 1
        ret = shutil.copyfile(each_picture, dst_file_path)
        if ret:
            total_file_count = total_file_count + 1
        #print(each_picture, "copied to ", dst_folder)
        bar.index = n + 1
        bar.update()
    bar.finish()
    print("\nCOPY %d files DONE, %d files overwrited, actually %d copied!" % (total_file_count, overwrite_count, (total_file_count-overwrite_count)))

if __name__ == '__main__':
    backup_pictures("/Users/junlin/Downloads", "/Users/junlin/myPhoto/Photography18/xxx", [".jpg", ".JPG", ".jpeg", ".JPEG", ".raf", ".RAF", ".png", ".PNG", ".PSD", ".psd"])