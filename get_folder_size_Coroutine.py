from os import path, walk, listdir, getcwd
import time
from gevent import monkey; monkey.patch_all()
import gevent


home_path = input("root 目录：\n")
if not path.isdir(home_path):
    raise Exception(f"{home_path} 不是一个文件夹")

print("正在递归遍历所有文件大小 时间有点长 去喝杯茶吧...")
start_time = time.time()

dirs = listdir(home_path)
dirTable = {}
details = []
threads = []

def get_file_totalSize(start_path,details,dirTable,dirInfo):
    total_size = 0
    root_level = start_path.count('\\')
    for dirpath, dirnames, filenames in walk(start_path):
        size = sum([path.getsize(path.join(dirpath, f))
                          for f in filenames])
        cur_level = dirpath.count('\\') - root_level
        total_size += size
        if dirpath != start_path:
            #加锁
            details.append([dirpath,size,cur_level])
            #解锁

    #加锁
    dirTable[start_path] = total_size
    dirInfo[1] = total_size
    #解锁

for f in dirs:
    dir = path.join(home_path,f)
    if path.isdir(dir):
        dirInfo = [dir,0,0]
        index = len(details)
        details.append(dirInfo)
        t1 = gevent.spawn(get_file_totalSize,dir,details,dirTable,dirInfo)
        threads.append(t1)
gevent.joinall(threads)

print("目录大小已统计完成 正在对齐结果排序...")
sortedList = []
if len(dirTable.keys()) > 0:
    sortedList = sorted(dirTable.items(), key=lambda x: x[1], reverse=True)

print("子目录大小排序结果:")
for f in sortedList:
    sizeContent = f"{f[1]/float(1024 * 1024)}MB" if f[1] > 1024 * 1024 else f"{f[1] / float(1024)}KB" if f[1] > 1024 else f"{f[1]}B"
    print(f"{f[0]}\t{sizeContent}")

print("-------------------------------")
print("正在将目录结构及占用详情写入本地txt文件中...")
if len(details) > 0:
    details_folder = path.join(getcwd(),"目录存储详情.txt")
    content = ""
    for f in details:
        sizeContent = f"{f[1]/float(1024 * 1024)}MB" if f[1] > 1024 * 1024 else f"{f[1] / float(1024)}KB" if f[1] > 1024 else f"{f[1]}B"
        lineContent = f"{f[0]} ({sizeContent})\n"
        for i in range(0,f[2],1):
            content += '\t'
        content += lineContent

    with open(details_folder,'w') as f:
        f.write(content)
    print(f"文件地址: {details_folder}")

print("----------程序运行结束----------")
print(f"运行时长: {time.time()-start_time}秒")
input("任意键退出")