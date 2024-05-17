import shutil

# 源文件路径
print('请输入源文件地址（斜杠统一为/）')
source_file = input()

# 目标文件路径
print('请输入目标文件地址（斜杠统一为/）')
destination_file = input()

# 复制文件
shutil.copy(source_file, destination_file)

print('文件复制成功！请输入字母z以结束进程。')
n=input()
if n == "z":
    print(' ')

