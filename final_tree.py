from ast import While
import ast
from re import A
from tkinter import Y
from tracemalloc import stop



class Tree:
    def __init__(self, data=None):
        self.data = data
        self.question = None
        self.yes = None
        self.no = None  # may leaf

    def unit_tree(self, tree):
        # unit_tree = Tree(tree)
        self.question = tree[0]
        self.yes = tree[1]
        self.no = tree[2]
        # return unit_tree

    def new_tuple(self):
        self.data = (self.question, self.yes, self.no)

xMasTree = \
    ("Do you want to watch a basketball game? ",
        ("Do you want to go to a tourist spot? ",
            ("Do you want to go to a restaraunt ",
                ("", None, None),
                ("", None, None)
            ),
            ("", None, None)
        ),
        ("",
            None, 
            None
        )
    )


def isLeaf(tree):
    if tree[1] == None and tree[2] == None:  # not internal node
        return True
    else:
        return False


def yes_no(ans):
    while True:
        right = ['yes', 'y', 'Y', 'Yes']
        left = ['n', 'no', 'N', 'No']
        if ans in right:
            return True
        elif ans in left:
            return False
        else:
            ans = input("Please enter 'yes', 'y', 'Y', 'Yes' or 'n', 'no', 'N', 'No'")
            continue


def Play(tree):
    """DOCSTRING!"""
    if isLeaf(tree):  # is leaf
        ans = input('What date do you want to go to the game? (MM/DD)')
        return ans
    else:
        # tree = unit_tree(tree)
        ans = input(tree[0])
        if yes_no(ans):
            a = Play(tree[1])
        else:
            if tree[0] == "Do you want to watch a basketball game? ":
                return "Bye"
            a = Play(tree[2])
        return a  # final return


def tree_reader():
    """DOCSTRING!"""
    # Write the "main" function for 20 Questions here.  Although
    # main() is traditionally placed at the top of a file, it is the
    # last function you will write.
    print('Welcome to Zoey\'s searching system')

    return Play(xMasTree)
    #print("The date of your plan is:", plan_date)
    

