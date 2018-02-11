import time
from threading import Thread

def gen_coroutine(f):
    def wrapper(*args, **kwargs):
        gen_f = f()  # gen_f为生成器req_a
        
        r = next(gen_f)  # r为生成器long_io
        def fun(g):
            ret=next(g) # 执行生成器long_io
            try:
                gen_f.send(ret) # 将结果返回给req_a并使其继续执行
            except StopIteration:
                pass
        t=Thread(target=fun,args=(r,));
        t.start();
    return wrapper

def long_io():
    print ("开始执行IO操作")
    time.sleep(5)
    print ("完成IO操作，yield回操作结果")
    yield "io result"

@gen_coroutine
def req_a():
    print("开始处理请求req_a") 
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
    # while 1:
    #     pass

if __name__ == '__main__':
    main()