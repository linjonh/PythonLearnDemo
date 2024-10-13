#### 装饰器test
def decor(func):
    def wrapper(*arg,**args):
        print("before decor")
        func(*arg,**args)
        print("after decor")
        return
    return wrapper

def dec2(fuc):
    def wrapper(*arg,**args):
        print("dec2")
        fuc(*arg,**args)
        return
    return wrapper

@decor
@dec2
def doSomething(arg,test,**args):
    print(f"dosomething:{arg} test={test} args={args}")
    return

if __name__=="__main__":
    doSomething(123,"deco logic",l23="hello")