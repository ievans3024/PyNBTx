#!/usr/bin/env python
# coding: utf-8

__author__ = 'ievans3024'
__version__ = '0.0.1'

from os import getcwd
from tkinter import BOTH, E, filedialog, LEFT, Menu, N, NW, PhotoImage, S, Tk, W
from tkinter.ttk import Button, Frame, Menubutton, Separator, Style, Treeview

# Tk instantiated outside of __main__ to allow use of Image classes for icon definitions
root = Tk()

# Icon definitions are necessary because widgets do not save data provided to the 'image' kwarg to the instance.
# To prevent image data from being garbage collected, they must exist in an external possible reference.
# TODO: replace 24px icons with 16px icons
icons = {
    'tags': {
        'byte': PhotoImage(file='icons/tag-byte.png'),
        'byte_array': PhotoImage(file='icons/tag-byte-array.png'),
        'compound': PhotoImage(file='icons/tag-compound.png'),
        'double': PhotoImage(file='icons/tag-double.png'),
        'float': PhotoImage(file='icons/tag-float.png'),
        'int': PhotoImage(file='icons/tag-int.png'),
        'int_array': PhotoImage(file='icons/tag-int-array.png'),
        'list': PhotoImage(file='icons/tag-list.png'),
        'long': PhotoImage(file='icons/tag-long.png'),
        'short': PhotoImage(file='icons/tag-short.png'),
        'string': PhotoImage(file='icons/text-plain.png'),
    },
    'actions': {
        'delete': PhotoImage(file='icons/list-remove.png'),
        'edit': PhotoImage(file='icons/gtk-edit.png'),
        'new': {
            'tag': {
                'byte': PhotoImage(file='icons/tag-byte-new.png'),
                'byte_array': PhotoImage(file='icons/tag-byte-array-new.png'),
                'compound': PhotoImage(file='icons/tag-compound-new.png'),
                'double': PhotoImage(file='icons/tag-double-new.png'),
                'float': PhotoImage(file='icons/tag-float-new.png'),
                'int': PhotoImage(file='icons/tag-int-new.png'),
                'int_array': PhotoImage(file='icons/tag-int-array-new.png'),
                'list': PhotoImage(file='icons/tag-list-new.png'),
                'long': PhotoImage(file='icons/tag-long-new.png'),
                'short': PhotoImage(file='icons/tag-short-new.png'),
                'string': PhotoImage(file='icons/tag-string-new.png'),
            }
        },
        'open': PhotoImage(file='icons/document-open.png'),
        'save': PhotoImage(file='icons/media-floppy.png'),
        'search': PhotoImage(file='icons/edit-find.png')
    }
}

OPEN_FILES = lambda: filedialog.askopenfilenames(initialdir=getcwd())
OPEN_FOLDER = lambda: filedialog.askdirectory(initialdir=getcwd())


class MainMenu(Menu):

    def __init__(self, parent):

        Menu.__init__(self, parent)

        self.parent = parent

        menu_file = Menu(self, tearoff=0)
        menu_file.add_command(label='New...')
        menu_file.add_command(label='Open...', command=OPEN_FILES)
        menu_file.add_command(label='Open Folder...', command=OPEN_FOLDER)
        # TODO: add "open minecraft save folder" option here
        # TODO: add separator here
        menu_file.add_command(label='Save...')
        # TODO: add "refresh" option here
        menu_file.add_separator()
        menu_file.add_command(label='Exit', command=root.quit)

        menu_edit = Menu(self, tearoff=0)
        menu_edit.add_command(label='Copy')
        menu_edit.add_command(label='Cut')
        menu_edit.add_command(label='Paste')
        # TODO: add separator here
        # TODO: add "rename", "edit" and "delete" options here
        # TODO: add separator here
        # TODO: add "move up" and "move down" options here

        # TODO: add "Search" top-level menu
        # [find] [find next] | [replace] | [chunk finder]

        # TODO: add "Help" top-level menu
        # [About]

        self.add_cascade(label='File', menu=menu_file)
        self.add_cascade(label='Edit', menu=menu_edit)


class ToolBar(Frame):

    def __init__(self, parent):

        Frame.__init__(self, parent)

        self.parent = parent

        elements = [
            Button(self, image=icons['actions']['open'], command=OPEN_FILES),
            # TODO: add "open folder" button here
            Button(self, image=icons['actions']['save']),
            # TODO: add "refresh content" button here
            Separator(self, orient='vertical'),
            # TODO: add "cut", "copy", "paste" buttons and another separator here
            Button(self, image=icons['actions']['search']),  # TODO: move this icon to the end of the toolbar
            # TODO: add "rename" button here
            Button(self, image=icons['actions']['edit']),
            Button(self, image=icons['actions']['delete']),
            Separator(self, orient='vertical'),
            Button(self, image=icons['actions']['new']['tag']['byte']),
            Button(self, image=icons['actions']['new']['tag']['short']),
            Button(self, image=icons['actions']['new']['tag']['int']),
            Button(self, image=icons['actions']['new']['tag']['long']),
            Button(self, image=icons['actions']['new']['tag']['float']),
            Button(self, image=icons['actions']['new']['tag']['double']),
            Button(self, image=icons['actions']['new']['tag']['byte_array']),
            Button(self, image=icons['actions']['new']['tag']['int_array']),
            Button(self, image=icons['actions']['new']['tag']['string']),
            Button(self, image=icons['actions']['new']['tag']['list']),
            Button(self, image=icons['actions']['new']['tag']['compound'])
        ]

        for e in elements:
            if isinstance(e, Separator):
                e.grid(row=0, column=elements.index(e), sticky=N+S, padx=6)
            else:
                e.grid(row=0, column=elements.index(e), padx=1)


class TreeDisplay(Treeview):

    class Node(object):

        def __init__(self):
            pass

        def add(self):
            pass

        def remove(self):
            pass

    def __init__(self, parent, **kwargs):

        # TODO: Store non-treeview kwargs locally, then strip out and pass the rest to Treeview.__init__()
        Treeview.__init__(self, parent, **kwargs)

        self.parent = parent


class MainWindow(Frame):

    def __init__(self, parent):

        Frame.__init__(self, parent)

        self.parent = parent
        self.parent.title('PyNBTx %s' % __version__)

        self.style = Style()
        self.style.theme_use('default')
        self.style.configure('TButton', padding=0)

        self.pack(fill=BOTH, expand=1)

        self.ui_init()

    def ui_init(self):

        menu = MainMenu(root)
        root['menu'] = menu

        toolbar = ToolBar(self)
        toolbar.pack(anchor=NW, padx=4, pady=4)

        tree = Treeview(self, height=20)
        tree.column('#0', width=300)
        tree.insert('', 'end', 'root', text='root')
        tree.insert('root', '0', 'one', text='one')
        tree.insert('one', '0', 'two', text='two')
        tree.insert('two', '0', 'three', text='three')
        tree.insert('three', '0', 'four', text='four')
        tree.insert('four', '0', 'five', text='five')
        tree.insert('five', '0', 'six', text='six')
        tree.insert('six', '0', 'seven', text='seven')
        tree.insert('seven', '0', 'eight', text='eight')
        tree.insert('eight', '0', 'nine', text='nine')
        tree.insert('nine', '0', 'ten', text='ten')
        tree.pack(fill=BOTH, anchor=NW, padx=4, pady=4)


def main():

    app = MainWindow(root)
    root.mainloop()

if __name__ == '__main__':
    main()