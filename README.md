# 1000 Essential English Words (Flash Cards)

This project favors a mostly functional programming style for data handling: loading, parsing, and transforming the word lists are implemented as small, composable functions with side effects limited to file I/O. The UI layer (Tkinter) orchestrates these functions and handles event-driven interactions.

## Features
- Simple flash-card GUI (front/back) for English–German vocabulary
- Tracks lists to learn and to repeat using local CSV files
- Image-based buttons for correct/incorrect actions
- Lightweight, offline, and easy to extend

## Project structure
- data/ — CSV word lists (e.g., english_words.csv, english_words_to_learn.csv, english_words_to_repeat.csv)
- images/ — UI assets (card faces, buttons)
- main.py — application entry point and logic

## Data format
- CSV files are semicolon-delimited: English;German
- Some files may not include a header row
- Example:
  ```
  work;Arbeit
  soul;Seele
  world;Welt
  ```

## Requirements
- Python 3.12+
- Standard library Tkinter (included on most systems)
- pandas (for CSV handling)
- pillow (for image loading)

Install dependencies:

## Run

## Development notes
- Keep data-loading and transformation logic in pure functions where possible.
- Guard file operations (existence, permissions) and validate inputs (e.g., minimum row counts) before use.
- Favor small, testable functions for parsing and filtering word lists; let the UI call into them.

## License
MIT. See the license section in the repository for details.