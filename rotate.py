from tkinter import LEFT, Toplevel,  Button, Label, Scale, RIGHT, HORIZONTAL
import tkinter as tk
import imutils
import cv2



class Rotate(Toplevel):
    def __init__(self, master=None):
        # khai báo một cửa sổ toplever
        Toplevel.__init__(self, master=master)
        
        #  khai báo các nút xoay thương dùng: 0, 90, 180, 270, 360 và thanh kéo chọn góc tuỳ chỉnh
        self.zero_button = Button(self, text="0")
        self.nighty_button = Button(self, text="90")
        self.one_hundred_eighty_button = Button(self, text="180")
        self.two_hundred_seventy_button = Button(self, text="270")
        self.three_hundred_sixty_button = Button(self, text="360")
        self.custom_label = Label(self, text="Custom")
        self.custom_scale = Scale(self, from_=0, to_=360, length=250, resolution=0.1, orient=HORIZONTAL)

        # khai báo 2 nút apply và cancel
        self.apply_button = Button(self, text="Apply")
        self.cancel_button = Button(self, text="Cancel")

        # gán sự kiện cho từng nút và hàm gọi đến tương ứng
        self.zero_button.bind("<ButtonRelease>", self.zero_button_released)
        self.nighty_button.bind("<ButtonRelease>", self.nighty_button_released)
        self.one_hundred_eighty_button.bind("<ButtonRelease>", self.one_hundred_eighty_button_released)
        self.two_hundred_seventy_button.bind("<ButtonRelease>", self.two_hundred_seventy_button_released)
        self.three_hundred_sixty_button.bind("<ButtonRelease>", self.three_hundred_sixty_button_released)
        self.apply_button.bind("<ButtonRelease>", self.apply_button_released)
        self.cancel_button.bind("<ButtonRelease>", self.cancel_button_released)

        # đặt vị trí cho các nút
        self.zero_button.pack(fill=tk.X, padx = 30, pady = 2)
        self.nighty_button.pack(fill=tk.X, padx = 30, pady = 2)
        self.one_hundred_eighty_button.pack(fill=tk.X, padx = 30, pady = 2)
        self.two_hundred_seventy_button.pack(fill=tk.X, padx = 30, pady = 2)
        self.three_hundred_sixty_button.pack(fill=tk.X, padx = 30, pady = 2)
        self.custom_label.pack(pady = 5)
        self.custom_scale.pack(padx = 30)
        self.cancel_button.pack(side=RIGHT, padx = 10, pady = 10)
        self.apply_button.pack(side=LEFT, padx = 10, pady = 10)

    # xoay 0 độ
    def zero_button_released(self, event):
        # self.master.processed_image = cv2.imread(self.original_image)

        # (h, w) = selfmaster.processed_image.shape[:2] 
        # center = (w // 2, h // 2)
        # M = cv2.getRotationMatrix2D(center, 0, 1.0)
        # self.master.processed_image = cv2.warpAffine(selfmaster.processed_image, M, (w, h))
        self.master.processed_image = imutils.rotate_bound(self.master.processed_image, 0)
        self.show_image()

    def nighty_button_released(self, event):
        self.master.processed_image = imutils.rotate_bound(self.master.processed_image, 90)
        self.show_image()

    def one_hundred_eighty_button_released(self, event):
        self.master.processed_image = imutils.rotate_bound(self.master.processed_image, 180)
        self.show_image()

    def two_hundred_seventy_button_released(self, event):
       self.master.processed_image = imutils.rotate_bound(self.master.processed_image, 270)
       self.show_image()

    def three_hundred_sixty_button_released(self, event):
        self.master.processed_image = imutils.rotate_bound(self.master.processed_image, 360)
        self.show_image()     

    def apply_button_released(self, event):
        # lấy giá trị độ cần xoay trên thanh scale
        degrees = int (self.custom_scale.get())
        self.master.processed_image = imutils.rotate_bound(self.master.processed_image, degrees)
        self.show_image()
        self.close()

    # khôi phục trạng thái ban đầu của ảnh khi chưa bị xoay
    def cancel_button_released(self, event):
        self.master.image_viewer.show_image(img=self.master.original_image)
        self.close()

    def show_image(self):
        self.master.image_viewer.show_image(img=self.master.processed_image)

    def close(self):
        self.destroy()
