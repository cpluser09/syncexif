import os
import sys
import shutil

FOLDER_SOURCE = "/Users/junlin/myPhoto"
FOLDER_DESTINATION = "/Users/junlin/myPhoto2"
FILE_FILTERS = [".jpg", ".JPG", ".jpeg", ".JPEG"]

def calc_dst_folder(source_file):
    file_with_sub_folder = source_file.replace(FOLDER_SOURCE, "")
    file_full_path = FOLDER_DESTINATION + file_with_sub_folder
    return file_full_path

def sync_file(source_file):
    dst_file = calc_dst_folder(source_file)
    if os.path.exists(dst_file) == True:
        return
    dst_folder,_ = os.path.splitext(dst_file)
    dst_folder = dst_folder[0: dst_folder.rfind("/")]
    if os.path.exists(dst_folder) == False:
        os.makedirs(dst_folder)
    shutil.copyfile(source_file, dst_file)

def search_files(root_name, filter, result):
    for dir_name in os.listdir(root_name):
        file_path = os.path.join(root_name, dir_name)
        if os.path.isdir(file_path):
            search_files(file_path, filter, result)
        else:
            file_name_with_path, ext = os.path.splitext(file_path)
            file_name = file_name_with_path [file_name_with_path.rfind("/")+1: len(file_name_with_path)]
            if ext in filter and file_name[0] != "." and "Trashes" not in file_name_with_path:
                sync_file(file_path)
                result.append(file_path)
    return result

def let_go():
    folder = FOLDER_SOURCE
    if os.path.exists(folder) == False:
        print("FOLDER_SOURCE not exist.", folder)
        return
    
    result = []
    
    result = search_files(folder, FILE_FILTERS, result)
    sorted(result)
    if len(result) == 0:
        print("No file found.")
        return

if __name__ == '__main__':
    let_go()