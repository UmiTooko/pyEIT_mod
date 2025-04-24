import time


def f(a):
    a+=4
    print("f(a) a: ",a)

def main():
    
    a=1
    while(1):
        f(a)
        print("main() a:",a)
        time.sleep(1)


if __name__ == "__main__":
    main()