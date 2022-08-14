class A:
    def __init__(self, v):
        self.a = v

    def run(self, v):
        self.a = v

    def link(self, x):
        self.next_class = x
        self.next_class.a = 10

a = A(1)
b = A(2)
a.a = 20
b.link(a)


print(a.a)
print(b.a)
print(b.next_class.a)