from os import path, walk, listdir, getcwd
import time
import threading


home_path = input("root 目录：\n")
if not path.isdir(home_path):
    raise Exception(f"{home_path} 不是一个文件夹")

print("正在递归遍历所有文件大小 时间有点长 去喝杯茶吧...")
start_time = time.time()

dirs = listdir(home_path)
details = []
threads = []
# R = threading.Lock()

def get_file_totalSize(root_path_url,root_info_data):
    total_size = 0
    root_level = root_path_url.count('\\')
    sub_dir_datas = root_info_data[2]
    for dirpath, dirnames, filenames in walk(root_path_url):
        size = sum([path.getsize(path.join(dirpath, f))
                          for f in filenames])
        cur_level = dirpath.count('\\') - root_level
        total_size += size
        if dirpath != root_path_url:
            sub_dir_datas.append([dirpath,size,cur_level])
            # info = [dirpath,size,cur_level]
            # #加锁
            # R.acquire()
            # if None != dirdict[dirpath]:
            #     dirdict[dirpath][2].append(info)
            # else:
            #     dirdict[dirpath] = info
            # #解锁
            # R.release()
    #加锁
    # R.acquire()
    root_info_data[1] = total_size
    #解锁
    # R.release()
for f in dirs:
    dir = path.join(home_path,f)
    if path.isdir(dir):
        dirroot = [dir,0,[]]
        details.append(dirroot)
        t1 = threading.Thread(target=get_file_totalSize,args=(dir,dirroot))
        threads.append(t1)
        t1.start()
# 这里类似await  只有所有线程执行完成后 才能继续执行后面的代码
for t in threads:
    t.join()

print(f"目录大小已统计完成 正在对齐结果排序...")
sortedList = []
if len(details) > 0:
    details.sort(key=lambda x: x[1],reverse=True)

print(f"子目录大小排序结果...")
for f in details:
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
        content += lineContent
        
        for child in f[2]:
            sizeContent = f"{child[1]/float(1024 * 1024)}MB" if child[1] > 1024 * 1024 else f"{child[1] / float(1024)}KB" if child[1] > 1024 else f"{child[1]}B"
            lineContent = f"{child[0]} ({sizeContent})\n"
            for i in range(0,child[2],1):
                content += '\t'
            content += lineContent

    with open(details_folder,'w',encoding="utf-8") as f:
        f.write(content)
    print(f"文件地址: {details_folder}")


print("----------程序运行结束----------")
print(f"运行用时: {time.time()-start_time}秒")
input("任意键退出")