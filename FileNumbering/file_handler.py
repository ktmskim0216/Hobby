import sys
import os
from operator import itemgetter

def get_files(path, ext = '', recursive = False):
    '''
    Read all files in path
    :param path: path for reading
    :return: absolute path of all files in directory list
    '''
    path_list = [path]

    while len(path_list) > 0:
        cpath = path_list.pop()
        with os.scandir(cpath) as it:
            for entry in it:
                if not entry.name.startswith('.') and entry.is_file():
                    if entry.name.endswith(ext):
                        yield entry.path
                    else:
                        if recursive == True:
                            path_list.append(entry.path)



def get_files_by_mtime(path):
    result = list()

    for fpath in get_files(path):
        mtime = os.stat(fpath).st_mtime_ns
        result.append((fpath, mtime))

    result.sort(key = itemgetter(1))

    return result