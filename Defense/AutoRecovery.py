import shutil
import os
import hashlib
import traceback 

# 遍历文件内容和哈希值

class ScanDir():
    def __init__(self,source,target,monitor):
        self.source = source
        self.target = target
        self.monitor = monitor
        self.file_hash = {}

    def get_all(self,path):
        files = os.listdir(self.source)
        for file in files:
            file_path =  os.path.join(self.source,file)
            if os.path.isdir(file_path):
                self.get_all(file_path) # 递归遍历所有文件夹
            else:
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        md5obj = hashlib.md5()
                        md5obj.update(content.encode("utf-8"))
                        self.file_hash[file_path] = md5obj.hexdigest() # 保存文件哈希
                except:
                    traceback.print_exc()
      #  print(self.file_hash)

    def recover(self):
      #  print('-------------------------')
        self.get_all(self.source)
        files = os.listdir(self.target) # 扫描html文件夹
        for file in files: # 与源文件夹做对比，文件是否发生变化
            source_file_path =  os.path.join(self.source,file)
            target_file_path =  os.path.join(self.target,file)
            # 判断是否被写入文件或文件被篡改
            
            if source_file_path in self.file_hash.keys(): 
                with open(target_file_path, 'r+', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    md5obj = hashlib.md5() # 每次必须重新生成md5obj，否则md5会叠加
                    md5obj.update(content.encode("utf-8"))
                    hash = md5obj.hexdigest() 
                    # print(source_file_path,'----',hash)
                    # 判断文件是否被篡改
                    if hash != self.file_hash[source_file_path]: 
                       # print(hash,'-----',self.file_hash[source_file_path])
                        print('文件内容:"' + target_file_path + '"被更改')
                        try:
                            path = os.path.dirname(target_file_path) # 目的目录
                            shutil.copy(source_file_path,path) # 拷贝恢复文件
                            print('文件:"' + target_file_path + '"已更新')
                        except:
                            traceback.print_exc()
            else:  #被新写入了文件 
                os.chdir(self.monitor) # 切换到监控目录
                if os.path.exists(file): # 判断新增的文件是否已存在
                    pass
                else:
                    try:
                        shutil.copy(target_file_path,self.monitor) # 将新增的文件复制到monitor文件夹
                        print('备份植入文件到：“',target_file_path,'”成功！')
                        os.remove(target_file_path) # 删除新增的文件
                        print('删除植入文件：“',target_file_path,'”成功！')
                    except:
                        traceback.print_exc()

            # 判断是否被删除了文件
        source_files = os.listdir(self.source) # 遍历源文件
        for source_file in source_files:
            if source_file not in files: # 源文件被删除
                print('文件：“',os.path.join(self.target,source_file),'”被删除')
                try:
                    path = os.path.dirname(os.path.join(self.target,source_file)) # 目的目录
                    shutil.copy(os.path.join(self.source,source_file),path) # 拷贝恢复文件
                    print('文件：“',os.path.join(self.target,source_file),'“同步成功！')
                except:
                    traceback.print_exc()
 
def main():
    source = 'C:/Users/admin/Desktop/images' # 备份的源文件
    target = 'C:/Users/admin/Desktop/target'   # 实时修改的目的文件
    monitor = 'C:/Users/admin/Desktop/monitor' # 保存被植入的文件
    while(True):
        obj = ScanDir(source,target,monitor)
        obj.recover()

if __name__ == '__main__':
    main()
    