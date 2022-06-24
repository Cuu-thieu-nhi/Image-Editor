from tkinter import LEFT, Toplevel, Label, Scale, Button, HORIZONTAL, RIGHT
import cv2


class AdjustFrame(Toplevel):
    def __init__(self, master=None):
        # khai báo cửa sổ toplever
        Toplevel.__init__(self, master=master)
        self.brightness_value = 0
        self.previous_brightness_value = 0
        self.original_image = self.master.processed_image
        self.processing_image = self.master.processed_image

        # khai báo các nhãn, nút và các thanh scale
        self.brightness_label = Label(self, text="Brightness")
        self.brightness_scale = Scale(self, from_=0, to_=2, length=250, resolution=0.1, orient=HORIZONTAL)
        self.r_label = Label(self, text="R")
        self.r_scale = Scale(self, from_=-100, to_=100, length=250, resolution=1, orient=HORIZONTAL)
        self.g_label = Label(self, text="G")
        self.g_scale = Scale(self, from_=-100, to_=100, length=250, resolution=1, orient=HORIZONTAL)
        self.b_label = Label(self, text="B")
        self.b_scale = Scale(self, from_=-100, to_=100, length=250, resolution=1,orient=HORIZONTAL)
        self.apply_button = Button(self, text="Apply")
        self.preview_button = Button(self, text="Preview")
        self.cancel_button = Button(self, text="Cancel")

        self.brightness_scale.set(1)

        # gán sự kiện cho nút
        self.apply_button.bind("<ButtonRelease>", self.apply_button_released)
        self.preview_button.bind("<ButtonRelease>", self.show_button_release)
        self.cancel_button.bind("<ButtonRelease>", self.cancel_button_released)

        # đặt vị trí cho các đối tượng
        self.brightness_label.pack()
        self.brightness_scale.pack()
        self.r_label.pack()
        self.r_scale.pack()
        self.g_label.pack()
        self.g_scale.pack()
        self.b_label.pack()
        self.b_scale.pack()
        self.cancel_button.pack(side=RIGHT, padx = 5, pady = 5)
        self.preview_button.pack(side=RIGHT, padx = 5, pady = 5)
        self.apply_button.pack(side=RIGHT, padx = 5, pady = 5)

    # lưu cấu hình hiện tại
    def apply_button_released(self, event):
        self.show_button_release(event)
        self.master.processed_image = self.processing_image
        self.close()

    def show_button_release(self, event):
        # đổi độ sáng của ảnh
        self.processing_image = cv2.convertScaleAbs(self.original_image, alpha=self.brightness_scale.get())
        
        # lấy các thuộc tính r, g, b của ảnh hiện tại
        b, g, r = cv2.split(self.processing_image)

        # đổi thuộc tính theo thuộc tính mới
        for b_value in b:
            cv2.add(b_value, self.b_scale.get(), b_value)
        for g_value in g:
            cv2.add(g_value, self.g_scale.get(), g_value)
        for r_value in r:
            cv2.add(r_value, self.r_scale.get(), r_value)

        #  gộp 3 thuộc tính thành ảnh
        self.processing_image = cv2.merge((b, g, r))
        self.show_image(self.processing_image)

    def cancel_button_released(self, event):
        self.close()

    def show_image(self, img=None):
        self.master.image_viewer.show_image(img=img)

    def close(self):
        self.show_image()
        self.destroy()
