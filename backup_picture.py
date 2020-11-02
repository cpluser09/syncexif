import os
import sys
import shutil

FOLDER_SOURCE = "/Volumes/FUJI"
FOLDER_DESTINATION = "/Users/junlin/myPhoto/Photography18/xxx"
FILE_FILTERS = [".jpg", ".JPG", ".jpeg", ".JPEG"]

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

def let_go():
    folder = FOLDER_SOURCE
    if os.path.exists(folder) == False:
        print("FOLDER_SOURCE not exist. ", folder)
        return
    
    result = []
    
    result = search_files(folder, FILE_FILTERS, result)
    sorted(result)
    if len(result) == 0:
        print("No file found.")
        return

    dst_folder = FOLDER_DESTINATION
    if os.path.exists(dst_folder) == False:
        os.makedirs(dst_folder)

    total_file_count = 0
    for each_picture in result:
        file_name = each_picture[each_picture.rfind("/")+1: len(each_picture)]
        shutil.copyfile(each_picture, dst_folder+"/"+file_name)
        total_file_count = total_file_count + 1
        print(each_picture, "copied to ", dst_folder)

    print("\nCOPY", total_file_count, "files DONE!!!")

if __name__ == '__main__':
    let_go()