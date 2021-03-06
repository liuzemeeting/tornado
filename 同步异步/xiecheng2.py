import time
from threading import Thread

gen = None # 全局生成器，供long_io使用

def gen_coroutine(f):
    def wrapper(*args, **kwargs):
        global gen
        gen = f()
        next(gen)
    return wrapper

def long_io():
    def fun():
        print ("开始执行IO操作")
        global gen
        time.sleep(5)
        try:
            print ("完成IO操作，并send结果唤醒挂起程序继续执行")
            # 使用send返回结果并唤醒程序继续执行
            gen.send("io result")  
        except StopIteration: # 捕获生成器完成迭代，防止程序退出
            pass
    t=Thread(target=fun,args=());
    t.start();


@gen_coroutine
def req_a():
    print ("开始处理请求req_a")
    ret = yield long_io()
    print ("ret: %s" % ret)
    print ("完成处理请求req_a")

def req_b():
    print ("开始处理请求req_b")
    time.sleep(2)
    print ("完成处理请求req_b")

def main():
    req_a()
    req_b()
    while 1:
        pass

if __name__ == '__main__':
    main()