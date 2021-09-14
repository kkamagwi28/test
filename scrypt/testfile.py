import time


class SomeClass:
    info = "you started downloading"
    info1= ''


    def update(self):
        self.info1 = 'You continue updating'
        time.sleep(3)

    def update2(self):
        self.info2 = 'last text'
        time.sleep(3)


a = SomeClass()
print(a.info)
a.update2()
a.update()
print(a.info1)

print(a.info2)