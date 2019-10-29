# 遍历文件，传入一个文件夹，将里面所有文件的路径打印出来(递归)

all_files = []


def getAllFiles(directory_path):
    import os
    for sChild in os.listdir(directory_path):
        sChildPath = os.path.join(directory_path, sChild)
        if os.path.isdir(sChildPath):
            getAllFiles(sChildPath)
        else:
            all_files.append(sChildPath)
    return all_files
