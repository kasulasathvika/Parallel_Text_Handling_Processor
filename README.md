# 🚀 Parallel Text Processing with Product Review Sentiment Analysis

## 📌 Project Overview
This project is a **Parallel Text Processing System** designed to analyze **product reviews** and determine their sentiment.  
It processes large datasets efficiently using **multithreading** and provides insights such as **positive, negative, and neutral sentiment distribution**.

The system also includes **search functionality, performance comparison, and visualization**, making it a complete data analysis tool.

---

## 🎯 Objectives
- Analyze large-scale product review datasets  
- Classify reviews into Positive, Negative, and Neutral  
- Improve performance using parallel processing  
- Provide interactive dashboard and search functionality  
- Store processed results in a database  

---

## 🛠️ Technologies Used
- Python  
- Streamlit  
- Pandas  
- Matplotlib  
- ThreadPoolExecutor (Multithreading)  
- SQLite  

---

## ⚡ Features

### 📂 File Upload
- Supports `.txt`, `.csv`, `.xlsx`, `.json` files  
- Handles empty and invalid files  

### ⚙️ Parallel Processing
- Uses ThreadPoolExecutor  
- Processes multiple reviews simultaneously  
- Compares Normal vs Parallel execution time  

### 😊 Sentiment Analysis
- Rule-based approach using predefined word lists  
- Counts positive and negative words  
- Calculates sentiment score  
- Classifies reviews as Positive, Negative, or Neutral  

### 📊 Dashboard
- Total number of reviews  
- Positive / Negative / Neutral counts  
- Pie chart visualization  
- Performance comparison  

### 🔍 Search Functionality
- Keyword-based search on product reviews  
- Displays matching records from database  
- Sentiment analysis is performed on user input query  

### 📥 Export Feature
- Download results as CSV  

### 📧 Email Feature
- Send summary report via email  

---

## 🧠 System Workflow
1. Upload product review dataset  
2. Preprocess text data  
3. Process reviews using parallel threads  
4. Perform sentiment analysis  
5. Store results in database  
6. Display dashboard and charts  
7. Search and analyze sentiment  

---

## 📂 Project Structure
project/
│
├── app.py          # Main application (UI + Logic)  
├── database.py     # Database operations  
├── README.md       # Documentation  
├── LICENSE         # MIT License  

---

## 🚀 How to Run

Install dependencies:
pip install streamlit pandas matplotlib

Run the application:
streamlit run app.py

Open in browser:
http://localhost:8501

---

## ⚠️ Edge Case Handling
- Empty file validation  
- Invalid file handling  
- Case-insensitive search  
- Punctuation handling using regex  
- Repeated word handling  
- Large dataset processing  

---

## 📈 Performance
- Compares normal vs parallel execution  
- Parallel processing improves speed for large datasets  

---

## 🧾 License
This project is licensed under the MIT License.

---

