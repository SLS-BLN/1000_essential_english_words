import tkinter as tk
import pandas as pd
from pathlib import Path


BACKGROUND_COLOR = "#B1DDC6"
PRESSED_COLOR = "#9FC7B1"
FLIP_DELAY_MS = 3000
TITLE_TAG = "card_title"
WORD_TAG = "card_word"
MINIMUM_WORDS_TO_LEARN = 20
_flip_timer_id = None
_flip_token = 0  # increments for each new card shown

# TODO: avoid state to be set in a global variable
#   - better solution would be to encapsulate state in a class
#   - tuple used to prevent accidental mutation
current_word: tuple[str, str] | None = None


# ---------------------------- DATA ------------------------------- #
def select_word_list():
    """Select the list of words to learn or repeat."""
    global df
    pathname = Path("data/english_words_to_repeat.csv")
    if pathname.is_file() and (tmp := pd.read_csv(pathname)).shape[0] > MINIMUM_WORDS_TO_LEARN:
        df = pd.read_csv('data/english_words_to_repeat.csv')
        print("repeat")
    else:
        df = pd.read_csv('data/english_words_to_learn.csv')
        print("learn")
    if 'word' not in df.columns or 'translation' not in df.columns:
        df[['word', 'translation']] = df.iloc[:, 0].str.split(';', n=1, expand=True)
        print(df)


def get_random_word() -> None:
    """Return a random [word, translation] pair as a list."""
    select_word_list()
    global current_word
    row = df.sample(1).iloc[0]
    word_to_translate = str(row["word"]).strip()
    word_translation = str(row["translation"]).strip()
    current_word = [word_to_translate, word_translation]

def learn_again():
    """Save the current word to the list of words to learn."""
    global current_word
    if not current_word:
        return
    with open('data/english_words_to_repeat.csv', 'a') as file:
        file.write(f'{current_word[0]};{current_word[1]}\n')
    show_new_word()


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
    global _flip_timer_id, _flip_token, current_word
    get_random_word()
    if not current_word:
        return

    word_to_translate, word_translation = current_word

    # Cancel any pending flip from previous presses
    if _flip_timer_id is not None:
        try:
            window.after_cancel(_flip_timer_id)
        except Exception:
            pass
        _flip_timer_id = None

    # Bump the token to invalidate older scheduled flips
    _flip_token += 1
    token = _flip_token

    # Show front
    canvas.itemconfig(card_image_id, image=card_front_image)
    canvas.itemconfig(TITLE_TAG, text="English Word", fill="black")
    canvas.itemconfig(WORD_TAG, text=word_to_translate, fill="black")

    # Schedule flip for this specific token
    _flip_timer_id = window.after(
        FLIP_DELAY_MS,
        lambda t=word_translation, tok=token: flip_card(t, tok)
    )

    # TODO: if df = repeat -> remove word from word_to_repeat file
    #   check df
    #   remove from repeat_file
    #   add to learn_file

def flip_card(translation: str, token: int):
    global _flip_timer_id, _flip_token
    # Ignore stale flips
    if token != _flip_token:
        return

    _flip_timer_id = None
    canvas.itemconfig(card_image_id, image=card_back_image)
    canvas.itemconfig(TITLE_TAG, text="Translation", fill="white")
    canvas.itemconfig(WORD_TAG, text=translation, fill="white")

wrong_image = tk.PhotoImage(file="./images/wrong.png")
wrong_button = tk.Button(
    image=wrong_image,
    highlightthickness=0,
    bg=BACKGROUND_COLOR,
    borderwidth=0,
    command=learn_again
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