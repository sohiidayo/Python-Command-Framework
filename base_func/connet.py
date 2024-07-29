from mian import *

@register_function(key = "debug1")
def debug():
    print("debug")

@register_function(key = "debug2")
def debug2():
    print("debug2")