from file_handler import (
    read_file,
    split_into_chunks,
    process_single,
    process_in_parallel,
    process_with_multiprocessing
)
from database import(
    create_table,
    insert_results,
    drop_index,
    create_index,
    measure_query_time

)

import time

if __name__ == "__main__":

    print("Starting Performance Comparison...")

    lines = read_file("data/large_text.txt")
    chunks = split_into_chunks(lines, chunk_size=100)

    print("Total reviews:", len(lines))
    print("Total chunks:", len(chunks))

    # -----------------------------
    # 1️⃣ Single Processing
    # -----------------------------
    start = time.time()
    results_single = process_single(chunks)
    end = time.time()
    print("Single Processing Time:", round(end - start, 4), "seconds")

    # -----------------------------
    # 2️⃣ ThreadPoolExecutor
    # -----------------------------
    start = time.time()
    results_thread = process_in_parallel(chunks)
    end = time.time()
    print("Threading Time:", round(end - start, 4), "seconds")

    # -----------------------------
    # 3️⃣ Multiprocessing
    # -----------------------------
    start = time.time()
    results_multi = process_with_multiprocessing(chunks)
    end = time.time()
    print("Multiprocessing Time:", round(end - start, 4), "seconds")

    create_table()
    start_insert=time.time()
    insert_results(results_thread)
    end_insert=time.time()
    print("Insert Time:",round(end_insert-start_insert,4),"seconds")


    print("Comparison Completed.")

    print("\n--- Query Performance WITHOUT Index ---")
    drop_index()
    measure_query_time()

    print("\n--- Query Performance WITH Index ---")
    create_index()
    measure_query_time()