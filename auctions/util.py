def say_hi_before_and_after(func, msg=None):
    print("hi")
    if(msg != None):
        func(msg.upper())
    else:
        func("My name is freddy".upper())
    print("hi")


def printer_not_special(msg):
    print(f'message is: {msg}')

say_hi_before_and_after(printer_not_special)

@say_hi_before_and_after
def printer(msg):
    print(f'message is: {msg}')





def makin_stuff(*args,**kwargs):
    def makin_inner(func):
        print("\n\nhi mom")
        func(kwargs['msg'].upper())
        print("bye mom")

    return makin_inner

@makin_stuff(msg=input("Enter something crazy:\n"))
def funky(msgs):
    print(f'Crazy... {msgs}')