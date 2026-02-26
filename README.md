# Python Parallel Text Handling Processor

## Project Objective

This project implements a structured text processing system to analyze large-scale product reviews using parallel processing and rule-based sentiment scoring.

The system reads a large text file, splits it into chunks, processes each chunk in parallel, applies sentiment rules, and stores structured results into a SQLite database.

---

## Text Domain Definition

This system processes **Product Review Text Data**.

It analyzes customer reviews to:

- Count positive words (good, excellent, amazing, happy, etc.)
- Count negative words (bad, issue, error, poor, slow, etc.)
- Calculate sentiment score:

  sentiment_score = positive_count - negative_count

- Detect important keywords related to product reviews (quality, delivery, service, price, etc.)

---

## Architecture Flow

The system follows this structured pipeline:

1. Read Input File  
2. Split Text into Configurable Chunks  
3. Process Chunks in Parallel (ThreadPoolExecutor)  
4. Apply Rule Engine (Sentiment Scoring)  
5. Store Processed Results in SQLite  
6. Display Final Summary  

Everything is controlled through main.py.

---

## Project Structure

parallel_text_handling_processor/

- main.py → Controls full pipeline  
- file_handler.py → File reading, chunking, rule engine, parallel logic  
- database.py → Database connection & insert operations  
- project_data.db → SQLite database  
- data/large_text.txt → Product review dataset  
- README.md  

---

## Where Parallel Processing Is Implemented

Parallel processing is implemented using:

ThreadPoolExecutor(max_workers=4)

- Each chunk is processed in parallel.
- max_workers=4 was selected based on system CPU capacity.
- This improves scalability for large input files.

---

## Where Rule Engine Is Implemented

The rule engine is implemented inside:

process_chunk()

It performs:

- Regex-based word cleaning  
- Positive word counting  
- Negative word counting  
- Sentiment score calculation  
- Keyword detection  

Regex used:

re.findall(r'\b\w+\b', text.lower())

This ensures punctuation does not affect word matching.

---

## Database Integration

After parallel processing:

- Each processed chunk result is stored in SQLite.
- executemany() is used for efficient bulk insertion.

Database table: processed_results

Columns:

- id  
- chunk_text  
- positive_count  
- negative_count  
- sentiment_score  
- detected_keywords  

---

## Configuration

Chunk size is configurable:

CHUNK_SIZE = 100

This allows the system to scale for different file sizes.

---

## Error Handling

The system includes exception handling for:

- File not found errors  
- Database connection errors  
- Empty file handling  

This improves robustness and reliability.

---

## How To Run The Project

1. Activate virtual environment:

venv\Scripts\activate

2. Run main file:

python main.py

3. View results:

- Summary displayed in terminal  
- Detailed chunk results stored in project_data.db  

---

## Example Output

Total lines: 1000  
Total chunks: 10  

--- Analysis Summary ---  
Total positive words: 750  
Total negative words: 750  
Overall sentiment score: 0  

---

## Scalability

If input file size increases:

- More chunks are automatically created  
- Thread pool processes chunks in parallel  
- Database stores structured results efficiently  

The system scales dynamically without modifying core logic.

---

## Conclusion

This project demonstrates:

- Structured pipeline architecture  
- Parallel processing using ThreadPoolExecutor  
- Rule-based sentiment engine  
- Database integration using SQLite  
- Configurable and scalable system design