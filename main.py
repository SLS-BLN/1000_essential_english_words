import tkinter as tk
import pandas as pd
import random
from pathlib import Path

BACKGROUND_COLOR = "#B1DDC6"
MINIMUM_WORDS = 20  # Threshold for using repeat

# Globals
df_repeat = pd.DataFrame(columns=["word", "translation"])
df_learn = pd.DataFrame(columns=["word", "translation"])
word_list_df = pd.DataFrame(columns=["word", "translation"])
current_card = {}
current_source = "learn"

# ---------------------------- FILE HANDLING ------------------------------- #
def load_lists():
    global df_repeat, df_learn
    repeat_path = Path("data/english_words_to_repeat.csv")
    learn_path = Path("data/english_words_to_learn.csv")

    # Load repeat list
    if repeat_path.is_file():
        df_repeat = pd.read_csv(repeat_path, delimiter=';', encoding='utf-8-sig')
        if df_repeat.shape[1] != 2:
            raise ValueError("Repeat file must have exactly two columns: word;translation")
        df_repeat.columns = ["word", "translation"]
    else:
        df_repeat = pd.DataFrame(columns=["word", "translation"])

    # Load learn-list
    df_learn = pd.read_csv(learn_path, delimiter=';', encoding='utf-8-sig')
    if df_learn.shape[1] != 2:
        raise ValueError("Learn file must have exactly two columns: English;German")
    df_learn.columns = ["word", "translation"]

def select_source():
    global word_list_df, current_source
    if len(df_repeat) > MINIMUM_WORDS:
        word_list_df = df_repeat
        current_source = "repeat"
        print(f"Repeat list has more than {MINIMUM_WORDS} words → Using repeat list")
    elif df_repeat.empty:
        word_list_df = df_learn
        current_source = "learn"
        print("Repeat list empty → Using learn list")
    else:
        word_list_df = df_learn
        current_source = "learn"
        print(f"Repeat list has {len(df_repeat)} words (≤ {MINIMUM_WORDS}) → Using learn list")

def initialize_word_list():
    load_lists()
    select_source()

def save_repeat_to_disk():
    repeat_path = Path("data/english_words_to_repeat.csv")
    repeat_path.parent.mkdir(parents=True, exist_ok=True)
    with open(repeat_path, 'w', encoding='utf-8') as file:
        file.write("word;translation\n")
        for _, row in df_repeat.iterrows():
            file.write(f"{row['word']};{row['translation']}\n")

def remove_word_from_repeat(word):
    global df_repeat
    df_repeat = df_repeat[df_repeat['word'] != word].reset_index(drop=True)
    save_repeat_to_disk()
    if current_source == "repeat" and df_repeat.empty:
        select_source()

# ---------------------------- FLASHCARD LOGIC ------------------------------- #
def next_card():
    global current_card, flip_timer, word_list_df
    window.after_cancel(flip_timer)

    # Auto-switch if the source is empty
    if current_source == "repeat" and df_repeat.empty:
        select_source()
    elif current_source == "learn" and df_learn.empty:
        if len(df_repeat) > 0:
            select_source()
        else:
            canvas.itemconfig(card_title, text="Done!", fill="black")
            canvas.itemconfig(card_word, text="No more words", fill="black")
            canvas.itemconfig(card_background, image=card_front_img)
            return

    active_df = df_repeat if current_source == "repeat" else df_learn
    if active_df.empty:
        canvas.itemconfig(card_title, text="Done!", fill="black")
        canvas.itemconfig(card_word, text="No more words", fill="black")
        canvas.itemconfig(card_background, image=card_front_img)
        return

    word_list_df = active_df
    current_card = random.choice(active_df.to_dict(orient="records"))
    canvas.itemconfig(card_title, text="English", fill="black")
    canvas.itemconfig(card_word, text=current_card["word"], fill="black")
    canvas.itemconfig(card_background, image=card_front_img)
    flip_timer = window.after(3000, flip_card)

def flip_card():
    canvas.itemconfig(card_title, text="German", fill="white")
    canvas.itemconfig(card_word, text=current_card["translation"], fill="white")
    canvas.itemconfig(card_background, image=card_back_img)

def known_word():
    if current_source == "repeat":
        remove_word_from_repeat(current_card["word"])
    next_card()

def learn_again():
    global df_repeat
    if current_source == "learn":
        if not ((df_repeat['word'] == current_card['word']).any()):
            df_repeat = pd.concat([df_repeat, pd.DataFrame([current_card])], ignore_index=True)
            save_repeat_to_disk()
    next_card()

# ---------------------------- UI SETUP ------------------------------- #
window = tk.Tk()
window.title("Flashcard App")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, flip_card)

canvas = tk.Canvas(width=800, height=526)
card_front_img = tk.PhotoImage(file="images/card_front.png")
card_back_img = tk.PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

cross_image = tk.PhotoImage(file="images/wrong.png")
unknown_button = tk.Button(image=cross_image, highlightthickness=0, command=learn_again)
unknown_button.grid(row=1, column=0)

check_image = tk.PhotoImage(file="images/right.png")
known_button = tk.Button(image=check_image, highlightthickness=0, command=known_word)
known_button.grid(row=1, column=1)

# ---------------------------- START ------------------------------- #
initialize_word_list()
next_card()

window.mainloop()
