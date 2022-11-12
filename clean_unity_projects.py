from os import path,remove,walk,system
from traceback import print_exception
import time
from shutil import rmtree 

def delFolder(url):
    '''
        删除文件夹
    '''
    if path.isdir(url):
        rmtree(url)
    else:
        remove(url)
 
# def get_file_size(start_path = '.'):
#     '''
#         获取文件大小
#     '''
    
#     total_size = 0
#     for dirpath, dirnames, filenames in os.walk(start_path):
#         for f in filenames:
#             fp = os.path.join(dirpath, f)
#             # skip if it is symbolic link
#             if not os.path.islink(fp):
#                 total_size += os.path.getsize(fp)
#     return total_size


home_path = input("放入Unity 工程目录：\n")

if not path.isdir(home_path):
    raise Exception(f"{home_path} 不是一个文件夹")
    
deleteDirs = []
# total_size = get_file_size(home_path)
print("正在遍历查找所有Unity项目 请稍等...")
for root, dirs, files in walk(home_path):
    if "Library" in dirs:
        libpath = path.join(root.replace('\\','/'),"Library")
        print(f"find one: {libpath}")
        deleteDirs.append(libpath)

waitKey = input("y: 确认清理  n: 取消 \n")
needCmdDir = []
if "y" in waitKey:
    count = 0
    total = len( deleteDirs )
    start_time = time.time()
    for dir in deleteDirs:
        
        try:
            delFolder(dir)
            print(f"已删除 {dir}")
        except PermissionError as e:
            try:
                print("正在尝试调用命令行 强制删除")
                system(f'del "{dir}" /F /Q')
                if not path.exists(dir):
                    print(f"已删除 {dir}")
                else:
                    print(f"删除文件 {e.filename} 被阻止。请稍后手动删除")
                    needCmdDir.append(e.filename)
            except:
                print(f"删除失败{dir}... 跳过 执行下一个")
        except:
            print_exception()
            print(f"删除失败{dir}... 跳过 执行下一个")

        count += 1
        print(f"当前进度: {count}/{total}")
    # print("正在计算已删除的文件总大小...")
    # nowfile_size = get_file_size(home_path)
    # print(f"删除之前: {total_size}Byte")
    # print(f"删除之后: {nowfile_size}Byte")
    # print(f"已删除的文件总大小: { ( total_size-nowfile_size ) / float(1024 * 1024) }MB")
    print("------------程序运行结束------------")
    print(f"用时: {time.time()-start_time}秒")
    if len( needCmdDir ) > 0 :
        print("------------------------------")
        print("以下文件或目录需要手动删除：")
        for dir in needCmdDir:
            print(dir)

input("\n\n【任意键退出\n")