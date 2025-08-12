import tkinter as tk
import pandas as pd
import time

BACKGROUND_COLOR = "#B1DDC6"
PRESSED_COLOR = "#9FC7B1"
FLIP_DELAY_MS = 3000
TITLE_TAG = "card_title"
WORD_TAG = "card_word"


# ---------------------------- DATA ------------------------------- #
df = pd.read_csv('data/english_words.csv')  # file uses "word;translation" in one column

if 'word' not in df.columns or 'translation' not in df.columns:
    df[['word', 'translation']] = df.iloc[:, 0].str.split(';', n=1, expand=True)
    print(df)

def get_random_word() -> list[str]:
    """Return a random [word, translation] pair as a list."""
    row = df.sample(1).iloc[0]
    word_pair = [str(row["word"]).strip(), str(row["translation"]).strip()]
    return word_pair

# ---------------------------- UI ------------------------------- #
window = tk.Tk()
window.title("1000 Essential English Words")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

canvas = tk.Canvas(window, width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_image = tk.PhotoImage(file="images/card_front.png")
card_back_image = tk.PhotoImage(file="images/card_back.png")
card_image_id = canvas.create_image(400, 263, image=card_front_image)


# Create the title and text items and keep their IDs so we can update them later
title_text_id = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"), fill="black")
word_text_id = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"), fill="black")

canvas.itemconfig(title_text_id, tags=(TITLE_TAG,))
canvas.itemconfig(word_text_id, tags=(WORD_TAG,))


canvas.grid(row=0, column=0, columnspan=2, pady=20)

def button_press(button):
    button.config(bg=PRESSED_COLOR)
    window.after(100, lambda: button.config(bg=BACKGROUND_COLOR))

def show_new_word():
    new_word = get_random_word()
    word_to_translate = new_word[0]
    word_translation = new_word[1]
    canvas.itemconfig(card_image_id, image=card_front_image)
    canvas.itemconfig(TITLE_TAG, text="English Word")
    canvas.itemconfig(WORD_TAG, text=word_to_translate)
    window.after(FLIP_DELAY_MS, lambda: flip_card(word_translation))

def flip_card(translation):
    canvas.itemconfig(card_image_id, image=card_back_image)
    canvas.itemconfig(TITLE_TAG, text="Translation")
    canvas.itemconfig(WORD_TAG, text=translation)


wrong_image = tk.PhotoImage(file="./images/wrong.png")
wrong_button = tk.Button(
    image=wrong_image,
    highlightthickness=0,
    bg=BACKGROUND_COLOR,
    borderwidth=0
)
wrong_button.bind('<Button-1>', lambda e: button_press(wrong_button))
wrong_button.grid(row=1, column=0)

ok_image = tk.PhotoImage(file="./images/right.png")
ok_button = tk.Button(
    image=ok_image,
    highlightthickness=0,
    bg=BACKGROUND_COLOR,
    borderwidth=0,
    command=show_new_word
)
ok_button.bind('<Button-1>', lambda e: button_press(ok_button))
ok_button.grid(row=1, column=1)

# Show an initial word
show_new_word()

window.mainloop()