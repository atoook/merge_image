import os
import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

class Application(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master.geometry("600x200")
        self.master.title('IMAGE MERGE APP')

        self.entry = [tk.Entry(self.master) for i in range(3)]

        self.menu_bar = tk.Menu(self.master)
        self.master.config(menu=self.menu_bar)

        self.create_widgets()

    def input(self, num,action):
        self.entry[num].insert(tk.END, action)

    def merge(self):
        def merge_image(img1,img2):
            for i in range(img1.shape[0]):
                for j in range(img1.shape[1]):
                    white = True
                    for k in range(img1.shape[2]):
                        if img1[i,j,k] != 255:
                            white  = False
                    if white:
                        for k in range(img1.shape[2]):
                            img1[i,j,k] = img2[i,j,k]

            return img1

        for i in range(len(self.image_list)-1):
            if i == 0:
                new_img = merge_image(self.image_list[i],self.image_list[i+1])
            else:
                new_img = merge_image(new_img,self.image_list[i+1])

        cv2.imwrite('./result.png', new_img)
        messagebox.showinfo('info', 'new image was saved')

    def load_image(self):
        self.image_list = []
        image_paths = [self.entry[i].get() for i in range(3)]
        for image_path in image_paths:
            if image_path != '':
                self.image_list.append(cv2.imread(image_path))

        if len(self.image_list) < 2:
            messagebox.showerror('ERROR', 'Please select more than 2 images')

        self.merge()

    def select_file(self,index):
        fTyp = [("","*")]
        iDir = os.path.abspath(os.path.dirname(__file__))
        file = filedialog.askopenfilename(filetypes = fTyp,initialdir = iDir)
        # 処理ファイル名の出力
        self.input(index,file)


    def create_widgets(self):
        file_menu = tk.Menu(self.menu_bar)
        file_menu.add_command(label='Exit', command=self.master.quit)
        self.menu_bar.add_cascade(label='File', menu=file_menu)

        for i in range(3):
            self.entry[i].grid(row=i+2, column=0, columnspan=10, pady=3)
            self.entry[i].focus_set()

        tk.Button(self.master, text='select', width=8,
                  command=lambda: self.select_file(0)).grid(row=2, column=20, columnspan=2)

        tk.Button(self.master, text='select', width=8,
                  command=lambda: self.select_file(1)).grid(row=3, column=20, columnspan=2)

        tk.Button(self.master, text='select', width=8,
                  command=lambda: self.select_file(2)).grid(row=4, column=20, columnspan=2)

        tk.Button(self.master, text='merge', width=6,
                  command=self.load_image).grid(row=5, column=10, columnspan=2)


if __name__ == '__main__':
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
