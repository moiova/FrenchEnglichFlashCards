from tkinter import *
from tkinter import messagebox
import pandas
import random
import os

data_as_dict = {}
current_card = {}

BACKGROUND_COLOR = "#B1DDC6"
TIMER = 5000


# ------------------ Buttons Listeners -----------------#


def failed():
    flip_to_front_side()


def remembered():
    # as long as the dict is not empty
    if data_as_dict:
        data_as_dict.remove(current_card)
        # save progress on file
        frame = pandas.DataFrame(data_as_dict)
        frame.to_csv("data/words_to_learn.csv")

        flip_to_front_side()

    else:  # no more entries available
        win.after_cancel(flip_timer)


# ------------------- flip the card ------------------#
def flip_to_back_side():
    canvas.itemconfig(canvas_image, image=back_image)
    canvas.itemconfig(language_id, text="English", fill="white")
    try:
        canvas.itemconfig(word_id, text=current_card["English"], fill="white")
    except KeyError:
        messagebox.showinfo(title="Congratulations!", message="Good job! All flash cards remembered!")


def flip_to_front_side():
    global flip_timer, current_card

    win.after_cancel(flip_timer)
    current_card = next_card()
    if current_card:
        canvas.itemconfig(canvas_image, image=front_image)
        canvas.itemconfig(language_id, text="French", fill="black")
        canvas.itemconfig(word_id, text=current_card["French"], fill="black")
        flip_timer = win.after(TIMER, flip_to_back_side)


# ------------------- read data from csv -------------#
def read_data_from_csv_as_dict():
    global data_as_dict

    try:
        data = pandas.read_csv("data/words_to_learn.csv")

    except FileNotFoundError:
        try:
            complete_data = pandas.read_csv("data/french_words.csv")
            data_as_dict = complete_data.to_dict(orient="records")
        except FileNotFoundError:
            messagebox.showerror(title="Error", message="File does not exist")
    except pandas.errors.EmptyDataError:
        messagebox.showerror("Error", message="No data available in the file")

    else:
        # consider all French words as keys and the corresponding english words as values
        data_as_dict = data.to_dict(orient="records")

        # OR (using a FOR loop)

        # for (index, row) in data.iterrows():
        #     data_as_dict[row.French] = row.English


# ------------------- generate next word -------------#
def next_card():
    # generate a number and get the key
    if data_as_dict:
        return random.choice(data_as_dict)
    else:  # no more entries available
        win.after_cancel(flip_timer)
        messagebox.showinfo(title="Congratulations!", message="Good job! French flash cards remembered!")
        # remove temp file
        try:
            os.remove("data/words_to_learn.csv")
        except FileNotFoundError:
            pass


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
language_id = canvas.create_text(400, 150, text="French", font=("Ariel", 38, "italic"))

word_id = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
flip_timer = win.after(0, flip_to_front_side)

canvas.config(bg=BACKGROUND_COLOR)
canvas.grid(column=0, row=0, columnspan=2)

right_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_image, highlightthickness=0, command=remembered)
right_button.grid(column=1, row=1)

false_image = PhotoImage(file="images/wrong.png")
false_button = Button(image=false_image, highlightthickness=0, command=failed)
false_button.grid(column=0, row=1)

flip_to_front_side()

win.mainloop()
