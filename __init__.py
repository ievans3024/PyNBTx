#!/usr/bin/env python
# coding: utf-8

__author__ = 'ievans3024'
__version__ = '0.0.1'

from tkinter import Tk, BOTH, PhotoImage
from tkinter.ttk import Frame, Style, Button

# This has to exist for references in class definitions
icons = {}


class ToolBar(Frame):
    pass


class TreeDisplay(Frame):
    pass


class MainWindow(Frame):

    def __init__(self, parent):

        Frame.__init__(self, parent)

        self.parent = parent
        self.parent.title('PyNBTx %s' % __version__)

        self.style = Style()
        self.style.theme_use('default')

        self.pack(fill=BOTH, expand=1)

        button = Button(self, image=icons['TAG']['byte'])
        button.pack()

    def ui_init(self):
        pass


def main():

    root = Tk()

    # TODO: Move this outside of main() or __main__ requirement
    icons['TAG'] = {
        'byte': PhotoImage(file='icons/tag-byte.png'),
        'new': {

        }
    }
    app = MainWindow(root)
    root.mainloop()

if __name__ == '__main__':
    main()