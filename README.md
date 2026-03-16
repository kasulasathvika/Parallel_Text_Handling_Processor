# Parallel Text Handling Processor

## Project Overview
The Parallel Text Handling Processor is a Python-based system designed to process large volumes of text efficiently using parallel computing techniques. The system reads large text or CSV files, performs rule-based sentiment analysis, and stores the processed results in a SQLite database.

The goal of this project is to demonstrate the advantages of parallel processing when handling large datasets.

---

## Features

- Large text/CSV file processing
- Parallel processing using threading and multiprocessing
- Rule-based sentiment analysis
- SQLite database storage
- Search functionality for processed reviews
- Export processed results to CSV
- Performance comparison between single processing, threading, and multiprocessing

---

## Technologies Used

- Python
- SQLite
- Concurrent Futures (ThreadPoolExecutor / ProcessPoolExecutor)
- CSV Module
- Git & GitHub

---

## Project Structure

parallel_text_handling_processor/

main.py              # Main program execution  
file_handler.py      # File reading and text processing  
database.py          # Database operations  
data/reviews.csv     # Input dataset  
exported_results.csv # Exported results  
project_data.db      # SQLite database  
README.md

---

## How the System Works

1. The system reads a large CSV/text dataset.
2. The text is divided into chunks.
3. Chunks are processed using parallel processing.
4. Rule-based sentiment analysis is applied.
5. Results are stored in a SQLite database.
6. Users can search reviews or export results to CSV.

---

## Sentiment Analysis Rules

The system uses a simple rule-based sentiment scoring approach.

Positive Words:
good, excellent, amazing, great, happy

Negative Words:
bad, poor, terrible, slow, worst

The sentiment score determines whether the review is Positive or Negative.

---

## Running the Project

Run the program using:

python main.py

Menu options:

1. Search Reviews
2. Export Results to CSV
3. Exit

---

## Example Output

('Bad service and poor response from the team', -3, 'Negative', '2026-03-14')

Showing first 10 results  
Total results: 20077

---

## Learning Outcomes

- Understanding parallel processing in Python
- Comparing threading vs multiprocessing
- Efficient database storage using SQLite
- Implementing rule-based sentiment analysis
- Handling large datasets

---

