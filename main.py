from tkinter import *
from tkinter import messagebox
import pandas
import random

data_as_dict = {}

BACKGROUND_COLOR = "#B1DDC6"
TIMER = 5000
current_fr_word = None

# ------------------ Buttons Listeners -----------------#


def failed():
    flip_to_front_side()


def remembered():
    # as long as the dict is not empty
    if data_as_dict:
        del data_as_dict[current_fr_word]
        flip_to_front_side()

    else:  # no more entries available
        win.after_cancel(flip_timer)
        messagebox.showinfo(title="Congratulations!", message="Good job! All flash cards remembered!")


# ------------------- flip the card ------------------#
def flip_to_back_side():
    canvas.itemconfig(canvas_image, image=back_image)
    canvas.itemconfigure(language_id, text="English")
    try:
        canvas.itemconfigure(word_id, text=f"{data_as_dict[current_fr_word]}")
    except KeyError:
        messagebox.showinfo(title="Congratulations!", message="Good job! All flash cards remembered!")


def flip_to_front_side():
    global flip_timer
    global current_fr_word

    win.after_cancel(flip_timer)
    current_fr_word = next_word()
    if current_fr_word:
        canvas.itemconfig(canvas_image, image=front_image)
        canvas.itemconfigure(language_id, text="French")
        canvas.itemconfigure(word_id, text=f"{current_fr_word}")
        flip_timer = win.after(TIMER, flip_to_back_side)
    else:
        messagebox.showinfo(title="Congratulations!", message="Good job! All flash cards remembered!")


# ------------------- read data from csv -------------#
def read_data_from_csv_as_dict():
    global data_as_dict

    try:
        data = pandas.read_csv("data/french_words.csv")
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="File does not exist")
    except pandas.errors.EmptyDataError:
        messagebox.showerror("Error", message="No data available in the file")

    else:
        # consider all French words as keys and the corresponding english words as values
        for (index, row) in data.iterrows():
            data_as_dict[row.French] = row.English

            # OR (instead of the FOR loop
        # data_as_dict = data.to_dict(orient="records")


# ------------------- generate next word -------------#
def next_word():
    # put all the keys in a list
    try:
        keys_list = list(data_as_dict.keys())
    except ValueError:
        # no more entries available
        messagebox.showinfo(title="Congratulations!", message="Good job! French flash cards remembered!")
    else:
        try:
            # generate a number and get the key
            next_word_x = keys_list[random.randint(0, len(keys_list) - 1)]
        except ValueError:
            return None
        else:
            return next_word_x


# -------------- display word on flash card ----------#
read_data_from_csv_as_dict()

# ------------------- GUI Setup ----------------------#
win = Tk()
win.title("Re-Flash")
win.config(bg=BACKGROUND_COLOR, padx=50, pady=50)

back_image = PhotoImage(file="images/card_back.png")
front_image = PhotoImage(file="images/card_front.png")

canvas = Canvas(width=800, height=526, highlightthickness=0)
canvas_image = canvas.create_image(400, 263, image=front_image)
language_id = canvas.create_text(400, 150, text="French", font=("Ariel", 48, "italic"))
current_fr_word = next_word()
word_id = canvas.create_text(400, 263, text=current_fr_word, font=("Ariel", 60, "bold"))
flip_timer = win.after(0, flip_to_front_side)

canvas.config(bg=BACKGROUND_COLOR)
canvas.grid(column=0, row=0, columnspan=2)

# TODO - find a way to disable a canvas from being displayed

right_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_image, highlightthickness=0, command=remembered)
right_button.grid(column=1, row=1)

false_image = PhotoImage(file="images/wrong.png")
false_button = Button(image=false_image, highlightthickness=0, command=failed)
false_button.grid(column=0, row=1)

win.mainloop()
