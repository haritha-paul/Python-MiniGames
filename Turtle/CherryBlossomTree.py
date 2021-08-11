import turtle
import random
from math import sqrt

DEBUG = False
BRANCH = 60
SUNR = 40
MAGIC = 12


class FloweringTree:
    def __init__(self):
        self.petal_count = 0
        self.petal_left_border = 0
        self.petal_right_border = 0
        self.turtle = turtle.Turtle()
        self.frame = turtle.Screen()
        if DEBUG:
            self.frame.tracer(0, 0)
        else:
            self.frame.tracer(3, 0)
        self.frame.bgcolor('wheat')
        self.turtle.up()

    def tree(self, branch_len):
        if branch_len > 3:
            if 8 <= branch_len <= 12:
                if random.randint(0, 2) == 0:
                    self.turtle.color('snow')
                else:
                    self.turtle.color('lightcoral')
                self.turtle.pensize(branch_len / 3)
            elif branch_len < 8:
                self.petal_count += 1
                cur_x = self.turtle.pos()[0]
                if cur_x < 0:
                    self.petal_left_border = min(self.petal_left_border, cur_x)
                else:
                    self.petal_right_border = max(self.petal_right_border, cur_x)
                if random.randint(0, 1) == 0:
                    self.turtle.color('snow')
                else:
                    self.turtle.color('lightcoral')
                self.turtle.pensize(branch_len / 2)
            else:
                self.turtle.color('sienna')
                self.turtle.pensize(branch_len / 10)

            # Draw the branch/leaf
            self.turtle.down()
            self.turtle.forward(branch_len)
            self.turtle.up()

            random_angle = 3 + 2 * MAGIC * random.random()
            random_length = MAGIC * random.random()

            self.turtle.right(random_angle)
            self.tree(branch_len - random_length)
            self.turtle.left(2 * random_angle)
            self.tree(branch_len - random_length)
            self.turtle.right(random_angle)

            # return to the root of this chile tree
            self.turtle.up()
            self.turtle.backward(branch_len)



    def the_sun(self, radius=30):
        start_pos = self.turtle.pos()
        self.turtle.forward(500)
        self.turtle.left(90)
        self.turtle.forward(300)
        self.turtle.down()
        self.turtle.color('red')
        self.turtle.begin_fill()
        self.turtle.circle(radius)
        self.turtle.end_fill()
        self.turtle.color('lightcoral')
        self.turtle.up()
        self.turtle.right(90)
        self.turtle.goto(start_pos)



    def draw(self):
        try:
            self.turtle.left(90)
            self.turtle.backward(250)
            self.the_sun(SUNR)
            self.tree(BRANCH)
            self.petal_count = self.petal_count // (int(sqrt(2 * MAGIC)))
            self.turtle.backward(100)
            self.turtle.color('wheat')
            self.turtle.down()
            self.turtle.forward(20)
            self.frame.exitonclick()
        except KeyboardInterrupt:
            print('Keyboard Interrupt.')


if __name__ == '__main__':
    flowering_tree = FloweringTree()
    flowering_tree.draw()