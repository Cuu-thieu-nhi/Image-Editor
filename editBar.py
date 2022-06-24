from tkinter import Frame, Button, LEFT
from tkinter import filedialog
from filterFrame import FilterFrame
from adjustFrame import AdjustFrame
from rotate import Rotate
import cv2

class EditBar(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master=master)

        # khai báo các nút: new, save, save as, crop, rotate, filter, rotate, adjust, clear
        self.new_button = Button(self, text="New")
        self.save_button = Button(self, text="Save")
        self.save_as_button = Button(self, text="Save As")
        self.crop_button = Button(self, text="Crop")
        self.rotate_button = Button(self, text="Rotate")
        self.filter_button = Button(self, text="Filter")
        self.adjust_button = Button(self, text="Adjust")
        self.clear_button = Button(self, text="Clear")

        # gán sự kiện cho các nút, các nút đều được gán cho sự kiện nhả chuột và gọi đến phương thức tương ứng
        self.new_button.bind("<ButtonRelease>", self.new_button_released)
        self.save_button.bind("<ButtonRelease>", self.save_button_released)
        self.save_as_button.bind("<ButtonRelease>", self.save_as_button_released)
        self.crop_button.bind("<ButtonRelease>", self.crop_button_released)
        self.rotate_button.bind("<ButtonRelease>", self.rotate_button_released)
        self.filter_button.bind("<ButtonRelease>", self.filter_button_released)
        self.adjust_button.bind("<ButtonRelease>", self.adjust_button_released)
        self.clear_button.bind("<ButtonRelease>", self.clear_button_released)

        # thiết lập vị trí cho các nút
        self.new_button.pack(side=LEFT)
        self.save_button.pack(side=LEFT)
        self.save_as_button.pack(side=LEFT)
        self.crop_button.pack(side=LEFT)
        self.rotate_button.pack(side=LEFT)
        self.filter_button.pack(side=LEFT)
        self.adjust_button.pack(side=LEFT)
        self.clear_button.pack()

    #  khi nhả nút new, mở 1 hình ảnh mới
    def new_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.new_button:
            # nếu đang bật tính năng crop thì sẽ tắt nó đi
            if self.master.is_crop_state: 
                self.master.image_viewer.deactivate_crop()

            # lấy tên file và nội dung hình ảnh
            filename = filedialog.askopenfilename()
            image = cv2.imread(filename)

            #  gán các thông tin cần thiết, copy lại ảnh để sau này có thể khôi phục
            if image is not None:
                self.master.filename = filename
                self.master.original_image = image.copy()
                self.master.processed_image = image.copy()
                self.master.image_viewer.show_image()
                self.master.is_image_selected = True

    #  khi nhả nút save, lưu lại hình ảnh hiện tại
    def save_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.save_button:
            # nếu đang bật tính năng crop thì sẽ tắt nó đi 
            if self.master.is_image_selected:
                if self.master.is_crop_state:
                    self.master.image_viewer.deactivate_crop()

                # lưu lại hình ảnh đang được xử lý hiện tại
                save_image = self.master.processed_image
                image_filename = self.master.filename
                cv2.imwrite(image_filename, save_image)

    #  khi nhả nút save as, lưu lại hình ảnh hiện tại thành 1 file mới
    def save_as_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.save_as_button:
            # nếu đang bật tính năng crop thì sẽ tắt nó đi
            if self.master.is_image_selected:
                if self.master.is_crop_state:
                    self.master.image_viewer.deactivate_crop()

                # lấy kiểu file cũ và mở cửa sổ save as
                original_file_type = self.master.filename.split('.')[-1]
                filename = filedialog.asksaveasfilename()
                filename = filename + "." + original_file_type

                # sau khi lấy được tên file, lưu ảnh
                save_image = self.master.processed_image
                cv2.imwrite(filename, save_image)

                self.master.filename = filename

    # sau khi nhả nút crop
    def crop_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.crop_button:
            if self.master.is_image_selected:
                # nếu đang bật crop sẵn thì tắt, còn đang tắt thì bật
                if self.master.is_crop_state:
                    self.master.image_viewer.deactivate_crop()
                else:
                    self.master.image_viewer.activate_crop()

    # sau khi nhả nút rotate
    def rotate_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.rotate_button:
            # nếu đang bật crop thì tắt nó đi
            if self.master.is_image_selected:
                if self.master.is_crop_state:
                    self.master.image_viewer.deactivate_crop()

                # gọi widget rotate
                self.master.rotate_frame = Rotate(master=self.master)
                self.master.rotate_frame.grab_set()

    # sau khi nhả nút filter
    def filter_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.filter_button:
            # nếu đang bật crop thì tắt nó đi
            if self.master.is_image_selected:
                if self.master.is_crop_state:
                    self.master.image_viewer.deactivate_crop()

                # gọi widget filter
                self.master.filter_frame = FilterFrame(master=self.master)
                self.master.filter_frame.grab_set()

    # sau khi nhả nút adjust
    def adjust_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.adjust_button:
            # nếu đang bật crop thì tắt nó đi
            if self.master.is_image_selected:
                if self.master.is_crop_state:
                    self.master.image_viewer.deactivate_crop()

                # gọi cửa sổ adjust
                self.master.adjust_frame = AdjustFrame(master=self.master)
                self.master.adjust_frame.grab_set()

    # sau khi nhả nút clear
    def clear_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.clear_button:
            # nếu đang bật crop thì tắt nó đi
            if self.master.is_image_selected:
                if self.master.is_crop_state:
                    self.master.image_viewer.deactivate_crop()

                # đổi ảnh đang được xử lý hiện tại thành ảnh ban đầu đã được lưu lại
                self.master.processed_image = self.master.original_image.copy()
                # hiển thị ảnh đó lên
                self.master.image_viewer.show_image()
    
