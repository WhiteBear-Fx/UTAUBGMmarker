import tkinter as tk
from tkinter import ttk


class ParameterFormWidget(ttk.Frame):
    def __init__(self, master, *args):
        super().__init__(master)
        self.label = ttk.Label(master)
