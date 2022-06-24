from tkinter import Frame, Canvas, CENTER, ROUND
from PIL import Image, ImageTk
import cv2


class ImageViewer(Frame):

    def __init__(self, master=None):
        # tạo 1 frame nền xám, rộng 600px, cao 400px
        Frame.__init__(self, master=master, bg="gray", width=600, height=400)

        self.shown_image = None
        self.x = 0
        self.y = 0
        # vị trí bắt đầu cắt
        self.crop_start_x = 0
        self.crop_start_y = 0
        # vị trí kết thúc cắt
        self.crop_end_x = 0
        self.crop_end_y = 0
        self.rectangle_id = 0
        self.ratio = 0

        # khai báo canvas để có thể vẽ hình, độ rộng bằng frame
        self.canvas = Canvas(self, bg="gray", width=600, height=400)
        self.canvas.place(relx=0.5, rely=0.5, anchor=CENTER)

    # xoá tất cả các hình vẽ trên canvas hiện tại, bao gồm hình ảnh, hình chữ nhật vẽ ra từ chức năng crop
    def clear_canvas(self):
        self.canvas.delete("all")

    def show_image(self, img=None):
        # xoá tất cả các hình vẽ trên canvas hiện tại
        self.clear_canvas()

        # nếu không có ảnh nào được truyền vào hàm, thì sẽ hiển thị ảnh được xử lý hiện tại, 
        # nếu có thì sẽ hiển thị ảnh được truyền vào
        if img is None:
            image = self.master.processed_image.copy()
        else:
            image = img

        # mở ảnh với không gian màu RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # lấy chiều dài và rộng của ảnh, lấy cả tỉ số của chúng nữa
        (height, width) = image.shape[:2]
        ratio = height / width

        new_width = width
        new_height = height

        #  nếu chiều dài hoặc rộng này lớn hơn chiều dài rộng của cửa sổ hiện tại thì sẽ phải nén ảnh
        if height > self.winfo_height() or width > self.winfo_width():
            if ratio < 1:
                new_width = self.winfo_width()
                new_height = int(new_width * ratio)
            else:
                new_height = self.winfo_height()
                new_width = int(new_height * (width / height))

        # nén ảnh theo kích thước mới
        self.shown_image = cv2.resize(image, (new_width, new_height))
        self.shown_image = ImageTk.PhotoImage(Image.fromarray(self.shown_image))

        self.ratio = height / new_height

        # tạo 1 ảnh mới trên canvas, có tâm ở vị trí new_width / 2 và new_height / 2, nội dung ảnh là show_image
        self.canvas.config(width=new_width, height=new_height)
        self.canvas.create_image(new_width / 2, new_height / 2, anchor=CENTER, image=self.shown_image)

    # hàm khởi động cắt
    def activate_crop(self):
        self.canvas.bind("<ButtonPress>", self.start_crop)
        self.canvas.bind("<B1-Motion>", self.crop)
        self.canvas.bind("<ButtonRelease>", self.end_crop)

        self.master.is_crop_state = True

    # hàm huỷ cắt
    def deactivate_crop(self):
        self.canvas.unbind("<ButtonPress>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease>")

        self.master.is_crop_state = False

    # lấy vị trí hiện tại của con trỏ khi click
    def start_crop(self, event):
        self.crop_start_x = event.x
        self.crop_start_y = event.y

    def crop(self, event):
        # nếu đã có 1 hình chữ nhật được vẽ, thì xoá nó đi
        if self.rectangle_id:
            self.canvas.delete(self.rectangle_id)

        # lấy vị trí của con chuột hiện tại
        self.crop_end_x = event.x
        self.crop_end_y = event.y

        # vẽ 1 hình chữ nhật có 2 đỉnh là điểm bắt đầu cắt và điểm hiện tại, độ dày bằng 1
        # đây sẽ là hình sau khi được cắt ra nếu thả chuột
        self.rectangle_id = self.canvas.create_rectangle(self.crop_start_x, self.crop_start_y,
                                                         self.crop_end_x, self.crop_end_y, width=1)

    # kết thúc quá trình cắt, lấy toạ độ cắt và cắt ảnh
    def end_crop(self, event):
        # kiểm tra 4 trường hợp có thể xảy ra về vị trí của 2 điểm bắt đầu và kết thúc, sau đó gán cho 4 biến vị trí
        if self.crop_start_x <= self.crop_end_x and self.crop_start_y <= self.crop_end_y:
            start_x = int(self.crop_start_x * self.ratio)
            start_y = int(self.crop_start_y * self.ratio)
            end_x = int(self.crop_end_x * self.ratio)
            end_y = int(self.crop_end_y * self.ratio)
        elif self.crop_start_x > self.crop_end_x and self.crop_start_y <= self.crop_end_y:
            start_x = int(self.crop_end_x * self.ratio)
            start_y = int(self.crop_start_y * self.ratio)
            end_x = int(self.crop_start_x * self.ratio)
            end_y = int(self.crop_end_y * self.ratio)
        elif self.crop_start_x <= self.crop_end_x and self.crop_start_y > self.crop_end_y:
            start_x = int(self.crop_start_x * self.ratio)
            start_y = int(self.crop_end_y * self.ratio)
            end_x = int(self.crop_end_x * self.ratio)
            end_y = int(self.crop_start_y * self.ratio)
        else:
            start_x = int(self.crop_end_x * self.ratio)
            start_y = int(self.crop_end_y * self.ratio)
            end_x = int(self.crop_start_x * self.ratio)
            end_y = int(self.crop_start_y * self.ratio)

        # tạo 2 lát x và y
        x = slice(start_x, end_x, 1)
        y = slice(start_y, end_y, 1)
        
        # gán ảnh được xử lý hiện tại bằng ảnh mới và hiển thị
        self.master.processed_image = self.master.processed_image[y, x]

        self.show_image()





