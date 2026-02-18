from file_handler import read_file, split_into_chunks, process_in_parallel
from database import create_table,insert_results


def main():
    print("Starting Product Review Analysis...\n")

    lines = read_file("data/large_text.txt")
    chunks = split_into_chunks(lines, chunk_size=100)

    print("Total lines:", len(lines))
    print("Total chunks:", len(chunks))
    

    results = process_in_parallel(chunks)
    create_table()
    insert_results(results)

    total_positive = sum(r["positive_count"] for r in results)
    total_negative = sum(r["negative_count"] for r in results)
    overall_score = total_positive - total_negative

    print("\n--- Analysis Summary ---")
    print("Total positive words:", total_positive)
    print("Total negative words:", total_negative)
    print("Overall sentiment score:", overall_score)

if __name__ == "__main__":
    main()