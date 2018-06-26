import sys

from file_handler import get_files_by_mtime, copy_files

def main(argv = sys.argv):
    '''
    Main function
    :param argv:
    :return:
    '''
    if len(argv) < 3:
        print('Need [SourcePath] [Prefix]')
        sys.exit(0)

    spath = argv[1]
    prefix = argv[2]

    path = get_files_by_mtime(spath)

    fnums = copy_files(path, prefix)

    print('{0} files copied from {1}'.format(fnums, spath))

    # TODO(LuHa): Preserve original files or not?
    print('Do you want preserve original files?')
    print('If you do not want to it, copied files are located in ./output/')

if __name__ == '__main__':
    sys.exit(main())
