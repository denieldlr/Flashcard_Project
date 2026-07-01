BACKGROUND_COLOR = "#B1DDC6"
from tkinter import *
from tkinter import messagebox
import random
import pandas

#-------------------------------FLIPPING THE CARDS-------------------------------#

def flip_card():
    canvas.itemconfig(card,image=flashcard_back)
    canvas.itemconfig(f_or_e, text="English",fill="white")
    canvas.itemconfig(fe_word, text=new_word["English"],fill="white")

#-------------------------------ACCESSING WORDS FROM CSV-------------------------------#

new_word = {}

try:
    data = pandas.read_csv("./data/words_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv("./data/french_words.csv")
except ValueError:
    data = pandas.read_csv("./data/french_words.csv")

data_dict = data.to_dict(orient="records")

def change_word():
    global new_word
    global timer
    window.after_cancel(timer)
    new_word = random.choice(data_dict)
    canvas.itemconfig(card, image=flashcard_front)
    canvas.itemconfig(fe_word,text=new_word["French"],fill="black")
    canvas.itemconfig(f_or_e, text="French",fill="black")
    timer = window.after(3000, func=flip_card)

#-------------------------------REMOVING KNOWN WORDS-------------------------------#

def remove_word():
    data_dict.remove(new_word)
    data = pandas.DataFrame(data_dict)
    data.to_csv("./data/words_to_learn.csv",index=False)
    change_word()

#-------------------------------UI SETUP-------------------------------#

window = Tk()
window.title("Flashcard Project")
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)

timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)

flashcard_front = PhotoImage(file="./images/card_front.png")
flashcard_back = PhotoImage(file="./images/card_back.png")
card = canvas.create_image(400,262,image=flashcard_front)
f_or_e = canvas.create_text(400,150,font=("Arial",40,"italic"))
fe_word = canvas.create_text(400,262,font=("Arial",60,"bold"))
canvas.grid(column=0,row=0, columnspan=2)

wrong_img = PhotoImage(file="./images/wrong.png")
wrong_button = Button(image=wrong_img, highlightthickness=0, command=change_word)
wrong_button.grid(column=0,row=1)
right_img = PhotoImage(file="./images/right.png")
right_button = Button(image=right_img,highlightthickness=0, command=remove_word)
right_button.grid(column=1,row=1)

change_word()

window.mainloop()