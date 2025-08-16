import tkinter as tk
import pandas as pd
import random
from pathlib import Path

BACKGROUND_COLOR = "#B1DDC6"
MINIMUM_WORDS = 20

# ---------------------- PURE FUNCTIONS ---------------------- #

def load_list(file_path, col_names):
    """
    Load a CSV file as a DataFrame.
    Returns an empty DataFrame with given column names if file does not exist.
    """
    path = Path(file_path)
    if not path.is_file():
        return pd.DataFrame(columns=col_names)
    df = pd.read_csv(path, delimiter=';', encoding='utf-8-sig')
    if df.shape[1] != 2:
        raise ValueError(f"{file_path} must have exactly 2 columns")
    df.columns = col_names
    return df

def save_list(df, file_path):
    """
    Save a DataFrame to disk as a CSV file.
    Always overwrites existing file and creates parent folders if needed.
    """
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, sep=';', index=False, encoding='utf-8-sig')

def select_source(df_repeat, df_learn, min_words=MINIMUM_WORDS):
    """
    Decide which list to use as the active source.
    Returns a tuple: (source_name, DataFrame).
    - If repeat list has more than min_words, use it.
    - Otherwise, default to learn list.
    """
    if len(df_repeat) > min_words:
        return "repeat", df_repeat
    return "learn", df_learn

def remove_word(df, word):
    """
    Return a new DataFrame without the given word entry.
    Does not modify the original DataFrame.
    """
    return df[df['word'] != word].reset_index(drop=True)

def add_word_if_not_present(df, word_entry):
    """
    Return a new DataFrame with the given word added,
    but only if it is not already present.
    """
    if not ((df['word'] == word_entry['word']).any()):
        return pd.concat([df, pd.DataFrame([word_entry])], ignore_index=True)
    return df

def pick_random_card(df):
    """
    Select a random record from the given DataFrame.
    Returns None if DataFrame is empty.
    """
    if df.empty:
        return None
    return random.choice(df.to_dict(orient="records"))

# ---------------------- STATE INITIALIZATION ---------------------- #

def init_state():
    """
    Load both repeat and learn lists, decide which to use,
    and return a dictionary holding the full application state.
    """
    df_repeat = load_list("data/english_words_to_repeat.csv", ["word", "translation"])
    df_learn = load_list("data/english_words_to_learn.csv", ["word", "translation"])
    source, active_df = select_source(df_repeat, df_learn)
    return {
        "df_repeat": df_repeat,
        "df_learn": df_learn,
        "current_source": source,
        "current_df": active_df,
        "current_card": {}
    }

# ---------------------- UI FUNCTIONS ---------------------- #

def update_card_display(card, front=True):
    """
    Update the visual flashcard:
    - If front=True, show the 'word' side.
    - If front=False, show the 'translation' side.
    - If card=None, show a 'Done' message.
    """
    if card is None:
        canvas.itemconfig(card_title, text="Done!", fill="black")
        canvas.itemconfig(card_word, text="No more words", fill="black")
        canvas.itemconfig(card_background, image=card_front_img)
        return
    if front:
        canvas.itemconfig(card_title, text="English", fill="black")
        canvas.itemconfig(card_word, text=card["word"], fill="black")
        canvas.itemconfig(card_background, image=card_front_img)
    else:
        canvas.itemconfig(card_title, text="German", fill="white")
        canvas.itemconfig(card_word, text=card["translation"], fill="white")
        canvas.itemconfig(card_background, image=card_back_img)

# ---------------------- EVENT HANDLERS ---------------------- #

def next_card_handler():
    """
    Select and display the next card.
    Cancels the current flip timer and restarts it for the new card.
    """
    global state, flip_timer
    window.after_cancel(flip_timer)

    # Possibly change the active list based on current state
    state["current_source"], state["current_df"] = select_source(state["df_repeat"], state["df_learn"])

    # Pick a card and update state
    card = pick_random_card(state["current_df"])
    state["current_card"] = card
    update_card_display(card, front=True)
    if card:
        flip_timer = window.after(3000, flip_card_handler)

def flip_card_handler():
    """Flip the current card to show the translation."""
    update_card_display(state["current_card"], front=False)

def known_word_handler():
    """
    Handle a known word:
    - If in repeat mode, remove it from the repeat list and save.
    - Then display the next card.
    """
    global state
    if state["current_source"] == "repeat":
        state["df_repeat"] = remove_word(state["df_repeat"], state["current_card"]["word"])
        save_list(state["df_repeat"], "data/english_words_to_repeat.csv")
    next_card_handler()

def learn_again_handler():
    """
    Handle an unknown word:
    - If in learn mode, add it to the repeat list and save.
    - Then display the next card.
    """
    global state
    if state["current_source"] == "learn":
        state["df_repeat"] = add_word_if_not_present(state["df_repeat"], state["current_card"])
        save_list(state["df_repeat"], "data/english_words_to_repeat.csv")
    next_card_handler()

# ---------------------- UI SETUP ---------------------- #

window = tk.Tk()
window.title("Flashcard App")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, flip_card_handler)

canvas = tk.Canvas(width=800, height=526)
card_front_img = tk.PhotoImage(file="images/card_front.png")
card_back_img = tk.PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

cross_image = tk.PhotoImage(file="images/wrong.png")
unknown_button = tk.Button(image=cross_image, highlightthickness=0, command=learn_again_handler)
unknown_button.grid(row=1, column=0)

check_image = tk.PhotoImage(file="images/right.png")
known_button = tk.Button(image=check_image, highlightthickness=0, command=known_word_handler)
known_button.grid(row=1, column=1)

# ---------------------- START APP ---------------------- #
state = init_state()
next_card_handler()

window.mainloop()
