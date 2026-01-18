# Heritage.compare

This project compares texts in English, French, and Spanish using the `bert-score` library. It reads the texts from a SQLite database, performs the comparison, and then updates the database with the similarity scores.

## Features

*   **Text Comparison:** Uses `bert-score` to compare texts and calculate similarity scores.
*   **Multilingual:** Supports English, French, and Spanish.
*   **Database Integration:** Reads data from and writes scores to a SQLite database.

## Requirements

The dependencies are listed in the `requirements.txt` file. The main libraries are:
*   `bert-score`
*   `evaluate`
*   `sqlalchemy`
*   `pandas`
*   `torch`
*   `transformers`
*   `nltk`

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/ScottSyms/Heritage.compare.git
    cd Heritage.compare
    ```

2.  Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

The main script is `compare.py`.

**IMPORTANT:** The script has a hardcoded path to a SQLite database: `sqlite://///Users/scottsyms/code/HeritageCanada/data/checkingtext.db`. You will need to change this path to point to your own database.

To run the script:
```bash
python compare.py
```

## Configuration

The script has two configuration flags at the top of the file:

*   `MISALIGN` (boolean): If `True`, the first text in the spreadsheet is compared against all the content. The first comparison is like text with the rest being mismatched.
*   `STOPWORDS` (boolean): If `True`, stopwords are removed from the text before comparison.

## License

This project is not licensed.