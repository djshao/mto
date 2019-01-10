# -*- coding: utf-8 -*-

def print_3():
    print('locals():', locals())
    for i in range(3):
        globals()['a%s'%i] = i**2
        #globals()['a{}'.format(i)] = i**2
    print(a0, a1, a2)
    print(locals())
    print(globals())
