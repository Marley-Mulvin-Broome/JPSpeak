from window import Window
from traceback import print_exc

if __name__ == '__main__':

    try:
        window = Window()
        window.run()
    except:
        with open("error.txt", "w") as f:
            print_exc(file=f)
