import os
import webbrowser
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from tkinter import filedialog
from PIL import Image, UnidentifiedImageError, ImageTk


class App(ctk.CTk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # window settings
        self.title("Image Watermarker with Python")
        self.geometry("1000x550")
        self.FONT = ("Bebas Neue", 30)
        self.icon_path = ImageTk.PhotoImage(file=os.path.join("images", "python_logo.png"))
        self.wm_iconbitmap()
        self.iconphoto(False, self.icon_path)
        self.resizable(False, False)

        # frames
        self.before_frame = ctk.CTkFrame(self, width=450, height=400, fg_color="green")
        self.after_frame = ctk.CTkFrame(self, width=450, height=400, fg_color="red")

        # images
        self.python_logo = ctk.CTkImage(Image.open("./images/python_logo.png"), size=(50, 50))
        self.linked_image = ctk.CTkImage(Image.open("./images/linkedin_image.png"))
        self.github_image = ctk.CTkImage(Image.open("./images/github_image.png"))
        self.image_before = None
        self.image_after = None
        self.watermark = None

        # buttons
        self.upload_btn = ctk.CTkButton(self, text="Upload Image", width=150, height=30, command=self.upload)
        self.upload_btn.place(x=840, y=510)
        self.save_btn = ctk.CTkButton(self, text="Save", width=150, height=30, command=self.save)

        # social buttons
        self.github_btn = ctk.CTkButton(self, width=50, height=20, command=self.open_github, image=self.github_image)
        self.github_btn.configure(text="GitHub")
        self.github_btn.place(x=300, y=520)
        self.linkedin_btn = ctk.CTkButton(self, width=50, height=20, command=self.open_linkedin,
                                          image=self.linked_image)
        self.linkedin_btn.configure(text="LinkedIn")
        self.linkedin_btn.place(x=390, y=520)

        # labels
        self.main_label = ctk.CTkLabel(self, text="Image Watermarker with Python ", font=self.FONT,
                                       compound=ctk.RIGHT)
        self.main_label.configure(image=self.python_logo)
        self.main_label.place(x=10, y=10)
        self.credits_label = ctk.CTkLabel(self, text="Made with ❤ by Mahmod Dello, Follow me on ➡").place(x=10, y=520)
        self.before_label_text = ctk.CTkLabel(self, text="Before", font=self.FONT)
        self.after_label_text = ctk.CTkLabel(self, text="After", font=self.FONT)
        self.image_before_label = None
        self.image_after_label = None

        # file
        self.filename = None

    def upload(self):
        self.filename = filedialog.askopenfilename(initialdir="", filetypes=[("Image File", [".png", ".jpg", ".jpeg"])])

        # on trying to re-upload and the user didn't select watermark, hide the frame
        if self.before_frame:
            self.before_label_text.place_forget()
            self.before_frame.place_forget()

        if self.after_frame:
            self.after_label_text.place_forget()
            self.after_frame.place_forget()

        # Destroy the existing label if it exists
        if self.image_before_label:
            self.image_before_label.destroy()

        try:
            image = Image.open(self.filename).convert("RGBA")
        except AttributeError:
            CTkMessagebox(title="Warning", message="You cancelled the operation, try uploading again", icon="warning")

        except UnidentifiedImageError:
            CTkMessagebox(title="Warning", message="You have selected a not supported file type!", icon="warning")

        else:
            self.main_label.place_forget()
            # image before: frame and label settings
            self.image_before = ctk.CTkImage(dark_image=image, size=(450, 400))
            self.image_before_label = ctk.CTkLabel(self.before_frame, text="", image=self.image_before)
            self.image_before_label.pack()
            self.before_label_text.place(x=200, y=30)
            self.before_frame.place(x=10, y=70)

            # image after settings
            self.apply_watermark()

    def apply_watermark(self):

        # on trying to re-upload after an image is saved, hides the after_frame
        if self.after_frame:
            self.after_label_text.place_forget()
            self.after_frame.place_forget()
        # warning message
        CTkMessagebox(title="Watermark Attention", message="Now you should upload your watermark", icon="info")
        water_mark_path = filedialog.askopenfilename(title="Select the Watermark",
                                                     filetypes=[("Images", [".png", ".jpg"])])
        # get watermark image
        try:
            self.watermark = Image.open(water_mark_path).convert("RGBA")
        except AttributeError:
            self.before_label_text.place_forget()
            self.before_frame.place_forget()
            CTkMessagebox(title="Warning", message="You cancelled the operation, try uploading again", icon="warning")
            self.main_label.place(x=10, y=10)

        except UnidentifiedImageError:
            self.before_label_text.place_forget()
            self.before_frame.place_forget()
            CTkMessagebox(title="Warning", message="You have selected a not supported file type!", icon="warning")
            self.main_label.place(x=10, y=10)

        else:
            # Destroy old label if exist
            if self.image_after_label:
                self.image_after_label.destroy()

            # open the image, apply the watermark and saves it
            self.image_after = Image.open(self.filename)
            self.image_after.paste(self.watermark, (0, 0), mask=self.watermark)

            # image after: ctk label and frame settings
            image_after_ctk = ctk.CTkImage(dark_image=self.image_after, size=(450, 400))
            self.image_after_label = ctk.CTkLabel(self.after_frame, text="", image=image_after_ctk)
            self.image_after_label.pack()
            self.after_label_text.place(x=740, y=30)
            self.after_frame.place(x=540, y=70)
            self.save_btn.place(x=670, y=510)

    def save(self):
        # user selects the path to save the image
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("Images", [".png", ".jpg"])])
        self.image_after.save(save_path)
        # checking if file is saved correctly in the path, and showing message boxes
        if os.path.exists(save_path):
            CTkMessagebox(title="Success", message="File was saved successfully in the specified directory.",
                          icon="check")
            self.destroy_components()
        else:
            CTkMessagebox(title="Success", message="File was saved successfully in the specified directory.",
                          icon="check")

    def destroy_components(self):
        self.after_label_text.place_forget()
        self.after_frame.place_forget()
        self.before_label_text.place_forget()
        self.before_frame.place_forget()
        self.after_frame.place_forget()
        self.save_btn.place_forget()
        self.main_label.place(x=10, y=10)

    @staticmethod
    def open_github():
        webbrowser.open(url="https://github.com/mahmouddello")

    @staticmethod
    def open_linkedin():
        webbrowser.open(url="https://www.linkedin.com/in/mahmoud-dello/")


if __name__ == '__main__':
    app = App()
    app.mainloop()
