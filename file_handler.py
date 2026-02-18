# with open("data/large_text.txt","w") as f:
#     for i in range(1000):
#         f.write(f".\n")
# print("1000 lines file created")

from concurrent.futures import ThreadPoolExecutor

positive_words = ["good", "excellent", "happy", "amazing", "perfect"]
negative_words = ["bad", "error", "fail", "issue", "poor", "slow"]
important_keywords = ["delivery", "quality", "service", "price", "support"]

def read_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.readlines()

def split_into_chunks(lines, chunk_size=100):
    chunks = []
    for i in range(0, len(lines), chunk_size):
        chunks.append(lines[i:i + chunk_size])
    return chunks


def process_chunk(chunk):
    text = " ".join(chunk).lower()
    words = text.split()

    positive_count = sum(word in positive_words for word in words)
    negative_count = sum(word in negative_words for word in words)

    sentiment_score = positive_count - negative_count

    detected_keywords = [word for word in important_keywords if word in text]

    return {
        "chunk_text": text,
        "positive_count": positive_count,
        "negative_count": negative_count,
        "sentiment_score": sentiment_score,
        "detected_keywords": ", ".join(detected_keywords)
    }
def process_in_parallel(chunks):
    with ThreadPoolExecutor() as executor:
        results=list(executor.map(process_chunk,chunks))
        return results