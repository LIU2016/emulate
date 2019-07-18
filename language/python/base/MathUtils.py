# coding=utf-8
""" python基础知识 """
""" 
    1,列表 = 数组
    2,字典 = map
    3,元祖 = 不可修改的数组 ，函数返回的结果集一般都是元祖。元组可以转列表
    4,函数 def定义 ，可以传参和return 
    5,定义类 class ，有OOP的思想
"""


class MathUtils:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def compare(self):
        if self.a > self.b:
            print("{} 大于 {}".format(self.a, self.b))
        elif self.a <= self.b:
            print("{} 小于等于 {}".format(self.a, self.b))
