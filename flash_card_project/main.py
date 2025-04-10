import pandas as pd
from tkinter import *
from PIL import Image, ImageTk
import random
BACKGROUND_COLOR = "#B1DDC6"

# ---------------GENERATING WORDS---------------- #
data_file = pd.read_csv("data/french_words.csv").to_dict(orient="records")


class Generate:
    def __init__(self):
        self.pick = ''
        self.chosen_word = ''
        self.translation = ''
        self.index = 0

    def generate_word(self):
        self.pick = random.choice(data_file)
        self.chosen_word = self.pick['French']
        self.translation = self.pick['English']
        self.index = data_file.index(self.pick)


generate = Generate()


def switch_to_translation():
    canvas.itemconfig(card, image=card_back)
    canvas.itemconfig(word, text=generate.translation, fill='white')
    canvas.itemconfig(language, text='English', fill='white')


def generating():
    global flip_timer
    window.after_cancel(flip_timer)
    canvas.itemconfig(card, image=card_front)
    canvas.itemconfig(language, text='French', fill='black')
    generate.generate_word()
    canvas.itemconfig(word, text=generate.chosen_word, fill='black')
    flip_timer = window.after(3000, switch_to_translation)


def right_click():
    del data_file[generate.index]
    generating()


def left_click():
    generating()


# -----------------------UI----------------------- #
window = Tk()
window.title('Flash Card')
window.config(pady=50, padx=50, bg=BACKGROUND_COLOR)
canvas = Canvas(width=300, height=200, bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)
flip_timer = window.after(3000, switch_to_translation)



def load_resize_image(image_file, width, height):
    # Function to load and resize image using PIL library
    image = Image.open(image_file)
    image = image.resize((width, height))
    photo = ImageTk.PhotoImage(image)
    return photo


card_front = load_resize_image("images/card_front.png", 300, 200)
card_back = load_resize_image("images/card_back.png", 300, 200)
card = canvas.create_image(150, 100, image=card_front)
language = canvas.create_text(150, 50, text='French', font=('Poppins', 15, 'normal'))
word = canvas.create_text(150, 100, text='', font=('Poppins', 30, 'bold'))

# Creating Button
right_image = load_resize_image("images/right.png", 50, 50)
right_button = Button(image=right_image, command=right_click, borderwidth=0, highlightthickness=0)
right_button.grid(row=1, column=1)

wrong_image = load_resize_image("images/wrong.png", 50, 50)
wrong_button = Button(image=wrong_image, command=left_click, borderwidth=0, highlightthickness=0)
wrong_button.grid(row=1, column=0)

generating()


window.mainloop()
