import importlib.util 
import os
def import_modules_from_dirs(directories):  
    """  
    从指定的目录列表中导入所有.py文件（不包括__init__.py）作为模块。  
  
    :param directories: 包含目录路径的列表  
    :return: None，但会动态地导入模块  
    """  
    for directory in directories:  
        # 确保目录存在  
        if not os.path.isdir(directory):  
            # 这里原本应该有错误处理，但现在只是忽略不存在的目录  
            continue  
  
        # 遍历指定目录下的所有文件和文件夹  
        for filename in os.listdir(directory):  
            # 忽略非.py文件和__init__.py文件  
            if filename.endswith('.py') and filename != '__init__.py':  
                # 构造模块名（去掉.py后缀）  
                module_name = filename[:-3]  
                # 构造模块规格（spec）  
                spec = importlib.util.spec_from_file_location(module_name, os.path.join(directory, filename))  
                # 如果模块规格存在，则导入模块  
                if spec is not None:  
                    module = importlib.util.module_from_spec(spec)  
                    spec.loader.exec_module(module)  