# with open("data/large_text.txt","w") as f:
#     for i in range(1000):
#         f.write(f"This is sample line number{i}\n")
# print("1000 lines file created")

from concurrent.futures import ThreadPoolExecutor

def read_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.readlines()

def split_into_chunks(lines, chunk_size=100):
    chunks = []
    for i in range(0, len(lines), chunk_size):
        chunks.append(lines[i:i + chunk_size])
    return chunks

def process_chunk(chunk):
    return len(chunk)

if __name__ == "__main__":
    lines = read_file("data/large_text.txt")
    chunks = split_into_chunks(lines)

    print("Total lines:", len(lines))
    print("Total chunks:", len(chunks))

    with ThreadPoolExecutor() as executor:
        results = list(executor.map(process_chunk, chunks))

    print("Parallel processing results:", results)