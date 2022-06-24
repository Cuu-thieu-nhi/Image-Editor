from tkinter import LEFT, Toplevel, Button, RIGHT
import tkinter as tk
import numpy as np
import cv2

class FilterFrame(Toplevel):
    def __init__(self, master=None):
        # khai báo 1 cửa sổ toplever
        Toplevel.__init__(self, master=master)
        self.original_image = self.master.processed_image
        self.filtered_image = None

        # Khai báo các nút dành cho các bộ lọc
        self.negative_button = Button(master=self, text="Negative")
        self.black_white_button = Button(master=self, text="Black White")
        self.sepia_button = Button(master=self, text="Sepia")
        self.emboss_button = Button(master=self, text="Emboss")
        self.gaussian_blur_button = Button(master=self, text="Gaussian Blur")
        self.median_blur_button = Button(master=self, text="Median Blur")
        self.cancel_button = Button(master=self, text="Cancel")
        self.apply_button = Button(master=self, text="Apply")

        # gán sự kiện cho các nút
        self.negative_button.bind("<ButtonRelease>", self.negative_button_released)
        self.black_white_button.bind("<ButtonRelease>", self.black_white_released)
        self.sepia_button.bind("<ButtonRelease>", self.sepia_button_released)
        self.emboss_button.bind("<ButtonRelease>", self.emboss_button_released)
        self.gaussian_blur_button.bind("<ButtonRelease>", self.gaussian_blur_button_released)
        self.median_blur_button.bind("<ButtonRelease>", self.median_blur_button_released)
        self.apply_button.bind("<ButtonRelease>", self.apply_button_released)
        self.cancel_button.bind("<ButtonRelease>", self.cancel_button_released)

        # thiết lập vị trí cho các nút
        self.negative_button.pack(fill=tk.X, padx = 10, pady = 2)
        self.black_white_button.pack(fill=tk.X, padx = 10, pady = 2)
        self.sepia_button.pack(fill=tk.X, padx = 10, pady = 2)
        self.emboss_button.pack(fill=tk.X, padx = 10, pady = 2)
        self.gaussian_blur_button.pack(fill=tk.X, padx = 10, pady = 2)
        self.median_blur_button.pack(fill=tk.X, padx = 10, pady = 2)
        self.cancel_button.pack(side=RIGHT, padx = 10, pady = 10)
        self.apply_button.pack(side=LEFT, padx = 10, pady = 10)

    def negative_button_released(self, event):
        self.negative()
        self.show_image()

    def black_white_released(self, event):
        self.black_white()
        self.show_image()

    def sepia_button_released(self, event):
        self.sepia()
        self.show_image()

    def emboss_button_released(self, event):
        self.emboss()
        self.show_image()

    def gaussian_blur_button_released(self, event):
        self.gaussian_blur()
        self.show_image()

    def median_blur_button_released(self, event):
        self.gaussian_blur()
        self.show_image()

    def apply_button_released(self, event):
        self.master.processed_image = self.filtered_image
        self.show_image()
        self.close()

    def cancel_button_released(self, event):
        self.master.image_viewer.show_image()
        self.close()

    # bộ lọc âm bản
    def negative(self):
        # bitwise_not đảo ngược giá trị màu trong ảnh
        self.filtered_image = cv2.bitwise_not(self.original_image)
    
    # bộ lọc trắng đen
    def black_white(self):
        # chuyển ảnh về màu xám
        self.filtered_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
        # nếu độ xám < 127 thì đổi thành đen, lớn hơn hoặc bằng thì đổi thành trắng
        (thresh, self.filtered_image) = cv2.threshold(self.filtered_image, 127, 255, cv2.THRESH_BINARY)

    # bộ lọc nâu đỏ
    def sepia(self):
        kernel = np.array([[0.272, 0.534, 0.131],
                           [0.349, 0.686, 0.168],
                           [0.393, 0.769, 0.189]])

        self.filtered_image = cv2.filter2D(self.original_image, -1, kernel)
    
    # bộ lọc nổi
    def emboss(self):
        kernel = np.array([[0, -1, -1],
                           [1, 0, -1],
                           [1, 1, 0]])

        self.filtered_image = cv2.filter2D(self.original_image, -1, kernel)

    # bộ lọc mờ
    def gaussian_blur(self):
        self.filtered_image = cv2.GaussianBlur(self.original_image, (41, 41), 0)
    
    # bộ lọc mờ trung bình
    def median_blur(self):
        self.filtered_image = cv2.medianBlur(self.original_image, 41)

    def show_image(self):
        self.master.image_viewer.show_image(img=self.filtered_image)

    def close(self):
        self.destroy()
