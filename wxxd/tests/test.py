class Foo(object):
        def __init__(self):
            self.val = 1


class Foo2(Foo):
    def __init__(self):
        super(Foo2,self).__init__()
        print(self.val)

foo2 = Foo2()