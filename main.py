import tkinter as tk
import pandas as pd

BACKGROUND_COLOR = "#B1DDC6"
PRESSED_COLOR = "#9FC7B1"
FLIP_DELAY_MS = 3000
TITLE_TAG = "card_title"
WORD_TAG = "card_word"
_flip_timer_id = None
_flip_token = 0  # increments for each new card shown

# ---------------------------- DATA ------------------------------- #
# english_words should not be changed - this is just a reference
# english_words_to is a copy of english_words and can be changed
# english_words_to_repeat contains a list of words the user doesn't know yet

# TODO: check if words_to_repeat exists and contains more than 20 words
#   if this the case use the file
#   else chose words_to_learn
df = pd.read_csv('data/english_words_to_learn.csv')  # file uses "word;translation" in one column

if 'word' not in df.columns or 'translation' not in df.columns:
    df[['word', 'translation']] = df.iloc[:, 0].str.split(';', n=1, expand=True)
    print(df)

def get_random_word() -> None:
    """Return a random [word, translation] pair as a list."""
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
    word_to_translate, word_translation = current_word
    print(word_to_translate, word_translation)
    # save both in the list english_words_to_repeat


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