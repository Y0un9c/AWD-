# coding=utf-8
import shutil
import os
import hashlib
import traceback
import argparse
import time


class ScanDir():
    def __init__(self, source, target, monitor, log):
        self.source = source
        self.target = target
        self.monitor = monitor
        self.log = log
        self.file_hash = {}

    def file_exits(self):
        if not os.path.exists(self.monitor):
            os.mkdir(self.monitor)
            print('mkdir monitor successfully')
        if not os.path.exists(self.log):
            fd = open(self.log, mode="w")
            fd.close()
            print('makefile log successfully')

    def get_all(self):
        for root, dirs, files in os.walk(self.source):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()
                        md5obj = hashlib.md5()
                        md5obj.update(content.encode("utf-8"))
                        # 保存文件哈希
                        self.file_hash[file_path] = md5obj.hexdigest()
                except:
                    traceback.print_exc()

    def check_changed(self):
        self.get_all()
        target_list = []
        for root, dirs, files in os.walk(self.target):  # 与源文件夹做对比，文件是否发生变化
            for file in files:
                target_file_path = os.path.join(root, file)
                target_list.append(target_file_path)
                source_file_path = target_file_path.replace(
                    self.target, self.source)
                source_file_path = os.path.normpath(source_file_path)

                # 判断是否被写入文件或文件被篡改
                if source_file_path in self.file_hash.keys():
                    with open(target_file_path, 'r+') as f:
                        content = f.read()
                        md5obj = hashlib.md5()  # 每次必须重新生成md5obj，否则md5会叠加
                        md5obj.update(content.encode("utf-8"))
                        hash = md5obj.hexdigest()
                        if hash != self.file_hash[source_file_path]:
                            print('file: "' + target_file_path + '" changed')
                            with open(self.log, 'ab+') as file_log:
                                file_log.write('{}----change file:{} \n'.format(time.strftime(
                                    "%Y-%m-%d %H:%M:%S", time.localtime()), target_file_path))
                            try:
                                path = os.path.dirname(
                                    target_file_path)  # 目的目录
                                shutil.copy(source_file_path, path)  # 拷贝恢复文件
                                print('file: "' + target_file_path +
                                      '" has been restored')
                            except:
                                traceback.print_exc()

                else:  # 被新写入了文件
                    os.chdir(self.monitor)  # 切换到监控目录
                    try:
                        # 将新增的文件复制到monitor文件夹
                        shutil.copy(target_file_path, self.monitor)
                        print('Backup planted file:"' +
                              target_file_path+'" successful')
                        with open(self.log, 'ab+') as file_log:
                            file_log.write('{}----Embedded file:{} \n'.format(time.strftime(
                                "%Y-%m-%d %H:%M:%S", time.localtime()), target_file_path))
                        os.remove(target_file_path)  # 删除新增的文件
                        print('delete planted file: "' +
                              target_file_path+'" successful')
                    except:
                        traceback.print_exc()

            # 判断是否被删除了文件
        for root, dirs, source_files in os.walk(self.source):
            for source_file in source_files:
                source = os.path.join(root, source_file).replace(
                    self.source, self.target)
                source = os.path.normpath(source)
                if source not in target_list:
                    print('file:"' + source + '"was deleted')
                    with open(self.log, 'ab+') as file_log:
                        file_log.write('{}----delete file:{} \n'.format(time.strftime(
                            "%Y-%m-%d %H:%M:%S", time.localtime()), source))
                    try:
                        path = os.path.dirname(source)  # 目的目录
                        if not os.path.exists(path):
                            os.mkdir(path)
                        shutil.copy(os.path.join(
                            root, source_file), path)  # 拷贝恢复文件
                        print('file: "' + source +
                              '" Synchronization succeeded')
                    except:
                        traceback.print_exc()


def main():
    parse = argparse.ArgumentParser(
        description='-s is required, and -m, -l and -t are optional. If -m and -l are not specified, monitor and log files are under /tmp by default, and target is /var/www/ by default')
    parse.add_argument('-s', type=str, help='Source file location')
    parse.add_argument('-t', type=str, default='/var/www/html/',
                       help='Target file location')
    parse.add_argument('-l', type=str, default='/tmp/log',
                       help='Log file location')
    parse.add_argument('-m', type=str, default='/tmp/monitor/',
                       help='New backup file location')
    args = parse.parse_args()
    source = args.s
    target = args.t
    log = args.l
    monitor = args.m
    if source[-1] != '/':
        source += '/'
    if monitor[-1] != '/':
        source += '/'
    if target[-1] != '/':
        source += '/'

    obj = ScanDir(source, target, monitor, log)
    obj.file_exits()
    while 1:
        obj.check_changed()

if __name__ == '__main__':
    main()
