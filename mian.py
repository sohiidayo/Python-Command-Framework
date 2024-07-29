import concurrent.futures  
import functools  
import threading  
import time

_initalized = False

def initalized():
    global _initalized
    if not _initalized:
        global function_registry
        function_registry = {}  
        # 线程池实例（如果需要使用线程池）  
        global executor
        executor = None  
        global max_workers
        max_workers=4
        executor = concurrent.futures.ThreadPoolExecutor(max_workers) 
        # global logger
        # logging.basicConfig(filename='log.txt', level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')  
        # logger = logging.getLogger(__name__) 
        _initalized = True

initalized()

# def catch_and_log_errors(func):  
#     """  
#     捕获被装饰函数抛出的异常，记录它们到日志文件中，并重新抛出异常。  
#     """  
#     @functools.wraps(func)  
#     def wrapper(*args, **kwargs):  
#         try:  
#             return func(*args, **kwargs)  
#         except Exception as e:  
#             # 记录异常信息到日志文件  
#             logger.error(f"Error in {func.__name__}: {e}")  
#             # 重新抛出异常  
#             raise  
#     return wrapper 

# def retry_decorator(max_retries=3, delay=1):  
#     """  
#     装饰器，用于在遇到错误时重新调用函数。  
  
#     :param max_retries: 最大重试次数  
#     :param delay: 每次重试前的延迟时间（秒）  
#     :return: 装饰后的函数  
#     """  
#     def decorator(func):  
#         @functools.wraps(func)  
#         def wrapper(*args, **kwargs):  
#             attempts = 0  
#             while attempts < max_retries:  
#                 try:  
#                     return func(*args, **kwargs)  
#                 except Exception as e:  
#                     attempts += 1  
#                     if attempts >= max_retries:  
#                         raise  # 如果达到最大重试次数，则重新抛出异常  
#                     time.sleep(delay)  # 等待一段时间后再重试  
#                     print(f"尝试 {attempts} 失败，将在 {delay} 秒后重试...")  
#             return None  # 理论上这里不应该被调用，除非函数正常返回None  
#         return wrapper  
#     return decorator 

# def log_execution_time(func):  
#     @functools.wraps(func)  
#     def wrapper_log_execution_time(*args, **kwargs):  
#         # 记录开始时间  
#         start_time = time.time()  
          
#         # 调用原函数  
#         result = func(*args, **kwargs)  
          
#         # 记录结束时间和运行时间  
#         end_time = time.time()  
#         run_time = end_time - start_time  
          
#         # 使用日志记录信息  
#         logger.info(f"Function {func.__name__} executed.")  
#         logger.info(f"Start Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))}")  
#         logger.info(f"End Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time))}")  
#         logger.info(f"Runtime: {run_time:.6f} seconds")  
          
#         # 返回原函数的返回值  
#         return result  
      
#     return wrapper_log_execution_time  
  
def register_function(key, use_threading=True, use_pool=True, callback=None):  
    """  
    装饰器函数，用于注册函数到全局字典，并支持多线程（直接创建或使用线程池）和回调函数。  
  
    :param key: 函数的唯一键  
    :param use_threading: 是否使用多线程（默认为 False）  
    :param use_pool: 是否使用线程池来管理线程（默认为 True），如果为 False，则直接为每个函数调用创建新线程  
    :param callback: 线程结束时调用的回调函数（默认为 None）  
    :return: 装饰后的函数  
    """  
    def decorator(func):  
        @functools.wraps(func)  
        def wrapper(*args, **kwargs):  
            if use_threading:  
                if use_pool:  
                    global executor
                    future = executor.submit(func, *args, **kwargs)  
                    future.add_done_callback(lambda f: callback(f.result()) if callback else None)  
                    return future  # 返回 Future 对象  
                else:  
                    # 直接为每个函数调用创建一个新线程  
                    def run_func():  
                        result = func(*args, **kwargs)  
                        
                        if callback:  
                            callback(result)  
  
                    thread = threading.Thread(target=run_func)  
                    thread.start()  
                    # 注意：这里没有直接的方式等待这个线程完成，除非使用 threading.Event 或其他同步机制  
            else:  
                result = func(*args, **kwargs)  
                
                if callback:  
                    callback(result)  
                return result  
  
        # 注册函数到全局字典  
        global function_registry
        function_registry[key] = wrapper  
        return wrapper  
  
    return decorator  
  
# 示例使用  
# @log_execution_time 
# @register_function("example_func", use_threading=True, use_pool=True)  
# def example_function(a, b):  
#     import time  
#     time.sleep(2)  # 模拟耗时操作  
#     return a + b  

  
# @register_function(key = "debug3")
# def debug3():
#     print("debug3")
  
# 调用被装饰的函数  


def shutdown_executor():  
    """  
    在程序结束时调用，以关闭线程池（如果有的话）。  
    注意：对于直接创建的线程，这个函数不会做任何事。  
    """  
    global executor  
    if executor is not None:  
        executor.shutdown(wait=True)  

# @log_execution_time 
# @register_function("example_func2", use_threading=True, use_pool=False)  
# @retry_decorator(max_retries=999999999, delay=10)  
# @catch_and_log_errors
# def test_network_connection():  
#     """  
#     模拟网络连接错误，3秒后抛出异常。  
#     """  
#     time.sleep(3)  # 模拟网络请求耗时  
#     raise ConnectionError("网络连接失败") 

# 通过字典调用函数  
if __name__ == "__main__":  

    #stest_network_connection()
    while 1:
        com = input("->")
        if com == "stop":
            break
        try:
            function_registry[com]()
        except Exception as e:
            print(e)
    # 在程序结束时调用（对于直接创建的线程，这不会等待它们完成）  
    shutdown_executor()  

  
