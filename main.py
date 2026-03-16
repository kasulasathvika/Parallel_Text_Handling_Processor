from file_handler import (
    read_file,
    read_csv_file,
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
    measure_query_time,
    search_reviews,
    export_to_csv

)

import time

if __name__ == "__main__":

    print("Starting Performance Comparison...")
    file_path="data/reviews.csv"
    if file_path.endswith(".csv"):
        lines=read_csv_file(file_path)
    else:
        lines=read_file(file_path)
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

    while True:

        print("\n----- MENU -----")
        print("1. Search Reviews")
        print("2. Export Results to CSV")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":

            keyword = input("Enter keyword (or press enter): ")
            sentiment = input("Enter sentiment Positive/Negative (or press enter): ")
            score = input("Minimum score (or press enter): ")

            score = int(score) if score else None
            sentiment = sentiment if sentiment else None
            keyword = keyword if keyword else None

            results = search_reviews(keyword, sentiment, score)
            if len(results)==0:
                print("No Matching reviews found")
            else:
                for row in results[:10]:
                    print(row)
                print("Showing first 10 rows")
                print("Total results:", len(results))

        elif choice == "2":

            export_to_csv()

        elif choice == "3":
            print("Exiting program")
            break