from tkinter import filedialog
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.ttk import Progressbar
import main
import cv2
import os
import shutil


def copy_file(source):
    image_name = os.path.basename(source)
    destination = 'test/test_items/' + image_name

    try:
        shutil.copy(source, destination)
        print("File Copied.")
    # eg. src and dest are the same file
    except shutil.Error as e:
        print('Error: %s' % e)
    # eg. source or destination doesn't exist
    except IOError as e:
        print('Error: %s' % e.strerror)


def browse():
    global folder_path
    filename = filedialog.askopenfilename(title="Select Image", filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
    folder_path.set(filename)
    txt_file_path.insert(0, filename)


def recognize():
    file = txt_file_path.get()
    copy_file(file)
    print(file)
    img = cv2.imread(file)
    cv2.imshow("meme", img)
    file_name = os.path.basename(file)
    sentence = main.recognize_image(file_name)

    txt_sentence.replace('1.0', END, sentence)
    messagebox.showinfo("Done", "Recognition Done !")


def analyze():
    print("Analyze Clicked !")


window = Tk()
window.title("Hate Content Detector - Team CodeX")

lbl_image = Label(window, text="Choose Image :", font=("Arial Bold", 12))
lbl_image.grid(column=0, row=1, sticky=W)

txt_file_path = Entry(window, width=45)
txt_file_path.grid(column=0, row=2, sticky=W, padx=5, pady=5)

btn_browse = Button(window, text="Browse", command=browse)
btn_browse.grid(column=1, row=2, sticky=E, padx=5, pady=5)

btn_recognize = Button(window, text="Recognize", command=recognize)
btn_recognize.grid(column=2, row=2, padx=5, pady=5)

lbl_text = Label(window, text="Generated Text :", font=("Arial Bold", 12))
lbl_text.grid(column=0, row=3, sticky=W)

txt_sentence = Text(window, width=50, height=5)
txt_sentence.grid(column=0, row=4, padx=5, pady=5, columnspan=3, sticky=W)

btn_analyze = Button(window, text="Analyze Text", command=analyze)
btn_analyze.grid(column=0, row=5, padx=5, pady=5, sticky=E, columnspan=3)

lbl_hate = Label(window, text="Hate Level :", font=("Arial Bold", 12))
lbl_hate.grid(column=0, row=6, sticky=W)

style = ttk.Style()
style.theme_use('clam')
style.configure("black.Horizontal.TProgressbar", background='red')
bar = Progressbar(window, length=300, style='black.Horizontal.TProgressbar')
bar['value'] = 70
bar.grid(column=0, row=7, sticky=W, columnspan=3, padx=5, pady=5)


lbl_category_label = Label(window, text="Category :", font=("Arial Bold", 12))
lbl_category_label.grid(column=0, row=8, sticky=W)


lbl_category = Label(window, text="Political", font=("Arial Bold", 12), background='yellow')
lbl_category.grid(column=0, row=9)

w = 430  # width for the Tk root
h = 350  # height for the Tk root

# get screen width and height
ws = window.winfo_screenwidth()  # width of the screen
hs = window.winfo_screenheight()  # height of the screen

# calculate x and y coordinates for the Tk root window
x = (ws / 2) - (w / 2)
y = (hs / 2) - (h / 2)

# set the dimensions of the screen
# and where it is placed
window.geometry('%dx%d+%d+%d' % (w, h, x, y))
folder_path = StringVar()
window.mainloop()
