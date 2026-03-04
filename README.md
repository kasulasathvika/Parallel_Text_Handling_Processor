# Parallel Text Handling Processor

## 📌 Project Overview

This project implements a **parallel text processing system** to analyze large product review datasets.  
It compares different processing techniques and evaluates database performance optimization using indexing.

The system demonstrates:

- Sequential Processing
- Multithreading (ThreadPoolExecutor)
- Multiprocessing
- Batch Database Insertion
- Index-based Query Optimization
- Performance Comparison

---

## 🚀 Features

### 1️⃣ Text Processing
- Reads large review dataset
- Splits data into configurable chunks
- Performs sentiment analysis
- Calculates sentiment score
- Labels reviews as Positive / Negative / Neutral

### 2️⃣ Parallel Execution
- Single-threaded processing
- Multithreading using ThreadPoolExecutor
- Multiprocessing using multiprocessing.Pool
- Performance comparison between all approaches

### 3️⃣ Database Optimization
- Stores processed results in SQLite database
- Uses batch insertion (executemany)
- Measures insert performance
- Creates and drops index on sentiment column
- Compares query performance with and without index

---

## 🛠 Technologies Used

- Python 3
- SQLite3
- ThreadPoolExecutor
- Multiprocessing
- VS Code

---

## 📂 Project Structure

```
parallel_text_handling_processor/
│
├── data/
│   └── large_text.txt
│
├── file_handler.py
├── database.py
├── main.py
├── generate_large_data.py
├── README.md
└── project_data.db (generated after run)
```

---

## ⚙️ How It Works

1. Read input file
2. Split into chunks (default chunk size = 100)
3. Process chunks using:
   - Sequential method
   - ThreadPoolExecutor
   - Multiprocessing
4. Compare execution times
5. Store results in SQLite database
6. Measure:
   - Insert time
   - Query time without index
   - Query time with index

---

## ▶️ How To Run

### Step 1: Activate Virtual Environment

Windows:
```
venv\Scripts\activate
```

### Step 2: Run Program
```
python main.py
```

---

## 📊 Example Output

```
Single Processing Time: 0.29 seconds
Threading Time: 0.31 seconds
Multiprocessing Time: 0.33 seconds
Insert Time: 0.10 seconds

--- Query Performance WITHOUT Index ---
Query Time: 0.0478 seconds

--- Query Performance WITH Index ---
Query Time: 0.0476 seconds
```

---

## 🧠 Performance Insights

- Threading performs well for I/O-bound tasks.
- Multiprocessing has overhead for smaller datasets.
- Batch insertion improves database performance.
- Indexing improves scalability for large datasets.
- With moderate dataset size, query difference may be minimal.

---

## 🎯 Learning Outcomes

- Understanding parallel processing in Python
- Comparing threading vs multiprocessing
- Efficient database insertion using executemany
- Index creation and query optimization
- Performance benchmarking


