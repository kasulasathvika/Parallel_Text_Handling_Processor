# Parallel Text Handling Processor

## Project Objective
This project is a structured text processing system designed to analyze large volumes of customer product reviews. The system performs chunk-based parallel processing, applies a rule-based sentiment engine, and stores results in a SQLite database.

---

## Text Domain
The system processes customer product reviews related to:
- Product quality
- Delivery
- Service
- Price
- Support

---

## System Architecture

Large Text File  
→ File Reader  
→ Chunk Splitter (100 lines per chunk)  
→ Parallel Processing (ThreadPoolExecutor)  
→ Rule-Based Sentiment Engine  
→ SQLite Database Storage  
→ Final Summary Output  

---

## Features Implemented

- Large file handling (1000 reviews)
- Configurable chunk processing
- Parallel processing using ThreadPoolExecutor
- Rule-based sentiment scoring
- Keyword detection
- SQLite database integration
- Structured main pipeline

---

## Rule Engine Logic

- Counts positive words
- Counts negative words
- Calculates sentiment score:

  sentiment_score = positive_count - negative_count

- Detects important keywords:
  delivery, quality, service, price, support

---

## Database Structure

Table: processed_results

Columns:
- id (Primary Key)
- chunk_text
- positive_count
- negative_count
- sentiment_score
- detected_keywords

---

## How to Run the Project

1. Activate virtual environment:
   venv\Scripts\activate

2. Run the main file:
   python main.py

---

## Technologies Used

- Python
- SQLite
- ThreadPoolExecutor (concurrent.futures)
- Git & GitHub

---

