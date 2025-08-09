BACKGROUND_COLOR = "#B1DDC6"
PRESSED_COLOR = "#9FC7B1"
import tkinter as tk


# ---------------------------- UI SETUP ------------------------------- #
window = tk.Tk()
window.title("1000 Essential English Words")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
canvas = tk.Canvas(width=800, height=526)

card_front_image = tk.PhotoImage(file="images/card_front.png")
canvas.create_image(400, 263, image=card_front_image)
canvas.create_text(400, 150, text="English Word", font=("Arial", 40, "italic"), fill="black")
canvas.create_text(400, 263, text="Translation", font=("Arial", 60, "bold"), fill="black")
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2, pady=20)

def button_press(button):
    button.config(bg=PRESSED_COLOR)
    window.after(100, lambda: button.config(bg=BACKGROUND_COLOR))

wrong_image = tk.PhotoImage(file="./images/wrong.png")
wrong_button = tk.Button(
    image=wrong_image,
    highlightthickness=0,
    bg=BACKGROUND_COLOR,
    borderwidth=0
)
wrong_button.bind('<Button-1>', lambda e: button_press(wrong_button))
wrong_button.grid(row=1, column=0)

right_image = tk.PhotoImage(file="./images/right.png")
right_button = tk.Button(
    image=right_image,
    highlightthickness=0,
    bg=BACKGROUND_COLOR,
    borderwidth=0
)
right_button.bind('<Button-1>', lambda e: button_press(right_button))
right_button.grid(row=1, column=1)

window.mainloop()