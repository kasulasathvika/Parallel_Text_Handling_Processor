# with open("data/large_text.txt","w") as f:
#     for i in range(1000):
#         f.write(f".\n")
# print("1000 lines file created")
import re
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool 
import os

positive_rules = {
    "excellent": 3,
    "amazing": 2,
    "good": 1,
    "happy": 2,
    "perfect": 2,
    "great": 2
}

negative_rules = {
    "terrible": -3,
    "bad": -1,
    "worst": -2,
    "error": -2,
    "poor": -2,
    "slow": -1
}
def read_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.readlines()
    except FileNotFoundError:
        print("Error: File not found.")
        return []

def split_into_chunks(lines, chunk_size=100):
    chunks = []
    for i in range(0, len(lines), chunk_size):
        chunks.append(lines[i:i + chunk_size])
    return chunks


def process_chunk(chunk):
    results = []

    for text in chunk:
        words = re.findall(r'\b\w+\b', text.lower())

        score = 0

        for word in words:
            if word in positive_rules:
                score += positive_rules[word]
            elif word in negative_rules:
                score += negative_rules[word]

        # Classification
        if score > 0:
            sentiment = "Positive"
        elif score < 0:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"

        results.append({
            "review_text": text.strip(),
            "score": score,
            "sentiment": sentiment
        })

    return results
def process_in_parallel(chunks):
    with ThreadPoolExecutor(max_workers=4) as executor:
        results=list(executor.map(process_chunk,chunks))
        return results
def process_single(chunks):
    results = []
    for chunk in chunks:
        results.append(process_chunk(chunk))
    return results
def process_with_multiprocessing(chunks):
    with Pool(processes=os.cpu_count()) as pool:
        results = pool.map(process_chunk, chunks)
    return results