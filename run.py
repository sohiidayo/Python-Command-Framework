import mian
import os
import sys
sys.path.append(os.getcwd())
import base_featuers.import_packages_dynamically as import_list
import_list.import_modules_from_dirs( ["./base_func", "./user_func","./base_featurs"]  )
#base_featuers 存放程序使用的函数
#base_func 存放常用的函数
#user_func 存放特定情况下使用的函数


if __name__ == "__main__":  
    while 1:
        com = input("->")
        if com == "stop":
            break
        try:
            mian.function_registry[com]()
        except Exception as e:
            print(e)  
    mian.shutdown_executor()  