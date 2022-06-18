# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import tkinter as tk
from tkinter import ttk

from structure.user_interface import UserInterface


class GUI(UserInterface):

    _root = None

    @classmethod
    def start(cls):

        _root = tk.Tk()
        _root.title('Glossanea')
        _root.columnconfigure(0, weight=1)
        _root.rowconfigure(0, weight=1)

        frame_intro = ttk.Frame(_root, padding='20 20 20 20')
        frame_intro.grid(column=0, row=0)  # , sticky=(Tk.N, Tk.W, Tk.E, Tk.S)
        frame_intro.columnconfigure(0, weight=1)
        frame_intro.rowconfigure(0, weight=1)

        intro_text = ('Glossanea is my favourite programme.\n'
                      'Good for practicing my English.')

        label = ttk.Label(frame_intro, text=intro_text)
        label.grid(column=0, row=0)  # , sticky=(Tk.N, Tk.W, Tk.E, Tk.S)
        label.columnconfigure(0, weight=1)
        label.rowconfigure(0, weight=1)
        label.grid_configure(padx=5, pady=5)

        _root.mainloop()
