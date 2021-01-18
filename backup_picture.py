import os
import sys
import shutil
from progress.bar import Bar
import exifread

class FancyBar(Bar):
    copy_speed = 0
    message = 'Syncing'
    fill = '*'
    suffix = '%(percent).1f%% - %(elapsed)ds [remaining %(remaining)d - total %(max)d - speed %(copy_speed)d MB/S]'

def query_shot_time(file_name):
    imgexif = open(file_name, 'rb')
    if imgexif is None:
        return ""

    shot_time = ""
    exif = exifread.process_file(imgexif)
    if "EXIF DateTimeOriginal" in exif.keys():
        shot_time = exif["EXIF DateTimeOriginal"].printable
    elif "Image DateTimeOriginal" in exif.keys():
        shot_time = exif["Image DateTimeOriginal"].printable

    if len(shot_time) > 0:
        shot_time = shot_time.replace(":", "").replace(" ", "")
    imgexif.close()
    return shot_time

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
    print("begin backup SD CARD files...")
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
    total_copied_size = 0
    for n in range(len(result)):
        each_picture = result[n]
        file_name = each_picture[each_picture.rfind("/")+1: len(each_picture)]
        dst_file_path = dst_folder + "/" + file_name

        shot_time = query_shot_time(each_picture)
        if len(shot_time) > 0:
            original_path, original_file_name = os.path.split(dst_file_path)
            output_name, output_ext_name = os.path.splitext(original_file_name)
            dst_file_path = original_path + "/" + output_name + "_" + shot_time + output_ext_name

        if os.path.exists(dst_file_path) == True:
            overwrite_count += 1
        ret = shutil.copyfile(each_picture, dst_file_path)
        if ret:
            total_file_count = total_file_count + 1
            total_copied_size += os.path.getsize(each_picture)
            if bar.elapsed != 0:
                bar.copy_speed = total_copied_size / 1024 / 1024 / bar.elapsed
        #print(each_picture, "copied to ", dst_folder)
        bar.index = n + 1
        bar.update()
    bar.finish()
    print("\nCOPY %d files DONE, %d files overwrited, actually %d copied to %s" % (total_file_count, overwrite_count, (total_file_count-overwrite_count), dst_folder))

if __name__ == '__main__':
    #backup_pictures("/Users/junlin/Downloads", "/Users/junlin/myPhoto/Photography19/20201121_武康路_武定西路", [".jpg", ".JPG", ".jpeg", ".JPEG", ".raf", ".RAF", ".png", ".PNG", ".PSD", ".psd", ".mp4", ".MP4", ".mov", ".MOV", ".dng", ".DNG"])
    backup_pictures("/Users/junlin/test/sync_src", "/Users/junlin/test/backup", [".jpg", ".JPG", ".jpeg", ".JPEG", ".raf", ".RAF", ".png", ".PNG", ".PSD", ".psd", ".mp4", ".MP4", ".mov", ".MOV", ".dng", ".DNG"])