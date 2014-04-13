#!/usr/bin/env python
# coding: utf-8

__author__ = 'ievans3024'
__version__ = '0.0.2'

from os import getcwd, getenv, walk
from os.path import expanduser, join
from sys import platform
from tkinter import BOTH, filedialog, Menu, N, NW, PhotoImage, S, Tk, messagebox
from tkinter.ttk import Button, Frame, Separator, Style, Treeview

import nbt

# Tk instantiated outside of __main__ to allow use of Image classes for icon definitions
root = Tk()

# Icon definitions are necessary because widgets do not save data provided to the 'image' kwarg to the instance.
# To prevent image data from being garbage collected, they must exist in an external possible reference.
icons = {
    'about': PhotoImage(file='icons/gnome-about-logo.png'),
    'actions': {
        'chunk_find': PhotoImage(file='icons/workspace-switcher.png'),
        'copy': PhotoImage(file='icons/edit-copy.png'),
        'cut': PhotoImage(file='icons/edit-cut.png'),
        'delete': PhotoImage(file='icons/list-remove.png'),
        'edit': PhotoImage(file='icons/gtk-edit.png'),
        'exit': PhotoImage(file='icons/system-log-out.png'),
        'move': {
            'down': PhotoImage(file='icons/go-down.png'),
            'right': PhotoImage(file='icons/go-next.png'),
            'up': PhotoImage(file='icons/go-up.png')
        },
        'new': {
            'generic': PhotoImage(file='icons/list-add.png'),
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
        'open': {
            'file': PhotoImage(file='icons/document-open.png'),
            'folder': PhotoImage(file='icons/folder-move.png'),
            'mc_folder': PhotoImage(file='icons/go-home.png')
        },
        'paste': PhotoImage(file='icons/edit-paste.png'),
        'refresh': PhotoImage(file='icons/view-refresh.png'),
        'rename': PhotoImage(file='icons/format-text-strikethrough.png'),
        'replace': PhotoImage(file='icons/edit-find-replace.png'),
        'save': PhotoImage(file='icons/media-floppy.png'),
        'search': PhotoImage(file='icons/edit-find.png')
    },
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
    }
}

loaded_files = {}


def open_files(get_files=()):
    global loaded_files
    loaded_files = {}
    if not get_files:
        get_files = filedialog.askopenfilenames(initialdir=getcwd())
    for f in get_files:
        try:
            loaded_files[f] = nbt.nbt.NBTFile(f)
        except OSError:
            messagebox.showwarning('Open File', '%s does not appear to be an NBT file.' % f)
            pass


def open_folder():
    global loaded_files
    filetree = walk(filedialog.askdirectory(initialdir=getcwd()))
    # TODO: make this examine every file in the tree, append valid nbt files to loaded_files list


def open_mc_dir():
    global loaded_files
    if str(platform) == 'windows':
        mc_parent = getenv('APPDATA')
    else:
        mc_parent = expanduser('~')

    mc_dir = join(mc_parent, '.minecraft', 'saves')
    get_files = filedialog.askopenfilename(initialdir=mc_dir)
    # TODO: decide if I want to open all savegame nbt files or just level.dat


def refresh_files():
    global loaded_files
    files = (f for f in loaded_files)
    open_files(get_files=files)


def save_files():
    global loaded_files
    for f in loaded_files:
        if isinstance(loaded_files[f], nbt.nbt.NBTFile):
            loaded_files[f].write_file()


class MainMenu(Menu):
    """
    Macro class for main window menus
    """
    def __init__(self, parent):

        Menu.__init__(self, parent)

        self.parent = parent

        menu_file = Menu(self, tearoff=0)
        menu_file.add_command(compound='left', image=icons['actions']['new']['generic'], label='New...')
        menu_file.add_command(compound='left',
                              image=icons['actions']['open']['file'], label='Open...', command=open_files)
        menu_file.add_command(compound='left',
                              image=icons['actions']['open']['folder'], label='Open Folder...', command=open_folder)
        menu_file.add_command(compound='left',
                              image=icons['actions']['open']['mc_folder'],
                              label='Open Minecraft Save Folder...', command=open_mc_dir)
        menu_file.add_separator()
        menu_file.add_command(compound='left', image=icons['actions']['save'], label='Save...', command=save_files)
        menu_file.add_command(compound='left', image=icons['actions']['refresh'],
                              label='Refresh', command=refresh_files)
        menu_file.add_separator()
        menu_file.add_command(compound='left', image=icons['actions']['exit'], label='Exit', command=root.quit)

        menu_edit = Menu(self, tearoff=0)
        menu_edit.add_command(compound='left', image=icons['actions']['copy'], label='Copy')
        menu_edit.add_command(compound='left', image=icons['actions']['cut'], label='Cut')
        menu_edit.add_command(compound='left', image=icons['actions']['paste'], label='Paste')
        menu_edit.add_separator()
        menu_edit.add_command(compound='left', image=icons['actions']['rename'], label='Rename')
        menu_edit.add_command(compound='left', image=icons['actions']['edit'], label='Edit')
        menu_edit.add_command(compound='left', image=icons['actions']['delete'], label='Delete')
        menu_edit.add_separator()
        menu_edit.add_command(compound='left', image=icons['actions']['move']['up'], label='Move Up')
        menu_edit.add_command(compound='left', image=icons['actions']['move']['down'], label='Move Down')

        menu_search = Menu(self, tearoff=0)
        menu_search.add_command(compound='left', image=icons['actions']['search'], label='Find')
        menu_search.add_command(compound='left', image=icons['actions']['move']['right'], label='Find Next')
        menu_search.add_separator()
        menu_search.add_command(compound='left', image=icons['actions']['replace'], label='Replace')
        menu_search.add_separator()
        menu_search.add_command(compound='left', image=icons['actions']['chunk_find'], label='Chunk Finder')

        menu_help = Menu(self, tearoff=0)
        menu_help.add_command(compound='left', image=icons['about'], label='About')

        self.add_cascade(label='File', menu=menu_file)
        self.add_cascade(label='Edit', menu=menu_edit)
        self.add_cascade(label='Search', menu=menu_search)
        self.add_cascade(label='Help', menu=menu_help)


class ToolBar(Frame):
    """
    Macro class for main window toolbar
    """
    def __init__(self, parent):

        Frame.__init__(self, parent)

        self.parent = parent

        elements = [
            Button(self, image=icons['actions']['open']['file'], command=open_files),
            Button(self, image=icons['actions']['open']['folder'], command=open_folder),
            Button(self, image=icons['actions']['save'], command=save_files),
            Button(self, image=icons['actions']['refresh'], command=refresh_files),
            Separator(self, orient='vertical'),
            Button(self, image=icons['actions']['cut']),
            Button(self, image=icons['actions']['copy']),
            Button(self, image=icons['actions']['paste']),
            Separator(self, orient='vertical'),
            Button(self, image=icons['actions']['rename']),
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
            Button(self, image=icons['actions']['new']['tag']['compound']),
            Separator(self, orient='vertical'),
            Button(self, image=icons['actions']['search'])
        ]

        for e in elements:
            if isinstance(e, Separator):
                e.grid(row=0, column=elements.index(e), sticky=N+S, padx=6)
            else:
                e.grid(row=0, column=elements.index(e), padx=1)


class TreeDisplay(object):
    """
    Acts as an intermediary between a treeview object and one or more nbt objects
    """

    def __init__(self, treeview, nbts=[], **kwargs):

        self.treeview = treeview
        self.nbts = nbts


class MainWindow(Frame):
    """
    Macro class for the main program window
    """
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