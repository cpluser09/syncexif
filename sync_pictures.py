import os
import sys
import shutil
import time
from progress.bar import Bar

global G_TOTAL_SYNC_COUNT

class FancyBar(Bar):
    message = 'Syncing'
    fill = '*'
    suffix = '%(percent).1f%% - %(elapsed)ds [remaining %(remaining)d - total %(max)d]'

import math

# class ProcessBar(object):
#     """一个打印进度条的类"""
#     def __init__(self, total):  # 初始化传入总数
#         self.shape = ['▏', '▎', '▍', '▋', '▊', '▉']
#         self.shape_num = len(self.shape)
#         self.row_num = 30
#         self.now = 0
#         self.total = total

#     def print_next(self, now=-1):   # 默认+1
#         if now == -1:
#             self.now += 1
#         else:
#             self.now = now
            
#         rate = math.ceil((self.now / self.total) * (self.row_num * self.shape_num))
#         head = rate // self.shape_num
#         tail = rate % self.shape_num
#         info = self.shape[-1] * head
#         if tail != 0:
#             info += self.shape[tail-1]
#         full_info = '[%s%s] [%.2f%%]' % (info, (self.row_num-len(info)) * '  ', 100 * self.now / self.total)

#         print("\r", end='', flush=True)
#         print(full_info, end='', flush=True)

#         if self.now == self.total:
#             print('')    

def calc_dst_folder(source_file, source_folder, dst_folder):
    file_with_sub_folder = source_file.replace(source_folder, "")
    file_full_path = dst_folder + file_with_sub_folder
    return file_full_path

def sync_file(source_file, source_folder, dst_folder):
    global G_TOTAL_SYNC_COUNT
    #print("\ntry sync:", source_file)
    dst_file = calc_dst_folder(source_file, source_folder, dst_folder)
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

def sync(files, source_folder, dst_folder):
    bar = FancyBar()
    bar.max = len(files)
    for n in range(len(files)):
        sync_file(files[n], source_folder, dst_folder)
        bar.index = n + 1
        bar.update()
    bar.finish()

def sync_pictures(source_folder, dst_folder, file_filters):
    print("begin sync files...")
    if os.path.exists(source_folder) == False:
        print("source folder not exist.", source_folder)
        return
    global G_TOTAL_SYNC_COUNT
    G_TOTAL_SYNC_COUNT = 0
    result = []
    result = search_files(source_folder, file_filters, result)
    sync(result, source_folder, dst_folder)
    print("DONE. total %d source files, %d files synced." % (len(result), G_TOTAL_SYNC_COUNT))
    # pb = ProcessBar(10000)
    # for i in range(10000):
    #     pb.print_next()

if __name__ == '__main__':
    sync_pictures("/Users/junlin/myPhoto", "/Users/junlin/myPhoto2", [".jpg", ".JPG", ".jpeg", ".JPEG", ".raf", ".RAF", ".png", ".PNG", ".PSD", ".psd", ".mp4", ".MP4", ".mov", ".MOV"])