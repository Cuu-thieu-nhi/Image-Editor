#khai báo các thư viện cần thiết
import tkinter as tk
from tkinter import ttk
from editBar import EditBar
from imageViewer import ImageViewer


class Main(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)

        # khai báo các thuộc tính chung của chương trình
        self.filename = ""
        self.original_image = None
        self.processed_image = None
        self.is_image_selected = False
        self.is_crop_state = False

        self.filter_frame = None
        self.adjust_frame = None

        self.title("Image Editor")

        # gọi 2 class EditBar và ImageViewer
        self.editbar = EditBar(master=self)
        self.image_viewer = ImageViewer(master=self)

        # gọi widget Separator
        separator1 = ttk.Separator(master=self, orient=tk.HORIZONTAL)

        # khai báo các thuộc tính tuỳ chỉnh
        self.editbar.pack(pady=10)
        separator1.pack(fill=tk.X, padx=20, pady=5)
        self.image_viewer.pack(fill=tk.BOTH, padx=20, pady=10, expand=1)

root = Main()
root.mainloop()