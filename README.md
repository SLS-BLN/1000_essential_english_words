# 1000 Essential English Words (Flash Cards)

This project implements a flash‑card learning app for English–German vocabulary.  
It favors a mostly functional programming style for data handling: loading, parsing, and transforming the word lists are implemented as small, composable functions with side effects limited to file I/O.  
The UI layer (Tkinter) orchestrates these functions and handles event‑driven interactions.

## 🧠 Implementations

- **`main.py`** – Original Code 1 version  
- **`main_ai.py`** – Updated, more functional refactor with a higher percentage of pure functions

## ✨ Features

- Simple flash‑card GUI (front/back) for English–German vocabulary  
- Tracks *learn* and *repeat* lists using local CSV files  
- Image‑based buttons for correct/incorrect actions  
- Lightweight, offline, and easy to extend  
- Two code paths to compare: baseline vs. refactored functional approach

## 📂 Project Structure

```
data/       # CSV word lists (e.g., english_words.csv, english_words_to_learn.csv, english_words_to_repeat.csv)
images/     # UI assets (card faces, buttons)
main.py     # Original application entry point and logic (Code 1)
main_ai.py  # Refactored functional version with more pure functions
```

## 📄 Data Format

- CSV files are semicolon-delimited: `English;German`  
- Some files may not include a header row

**Example:**

```
work;Arbeit
soul;Seele
world;Welt
```

## 🛠 Requirements

- Python 3.12+  
- Standard library **Tkinter** (included on most systems)  
- **pandas** (for CSV handling)  
- **pillow** (for image loading)

**Install dependencies:**

```bash
pip install pandas pillow
```

## ▶️ Run

```bash
# Run original Code 1 version
python main.py

# Run updated functional version
python main_ai.py
```

## 💡 Development Notes

- Keep data-loading and transformation logic in pure functions where possible  
- Guard file operations (existence, permissions) and validate inputs (e.g., minimum row counts) before use  
- Favor small, testable functions for parsing and filtering word lists; let the UI call into them  
- Compare `main.py` and `main_ai.py` to see the impact of reducing side effects and improving separation of concerns

## 🛠 Design Improvements in `main_ai.py`

Compared to the original `main.py`, the updated `main_ai.py`:

- Consolidates global state into a single state dictionary passed between functions  
- Splits logic into pure functions (`load`, `save`, `select`, `add`, `remove`, `pick`) for easier testing  
- Separates UI rendering from data manipulation for clearer boundaries  
- Adds more robust file handling and validation while keeping core logic simple  
- Improves overall readability and adaptability to new languages or data formats

This makes `main_ai.py` more modular, testable, and easier to extend without touching unrelated parts of the code.

## 📜 License

MIT. See the license section in the repository for details.
