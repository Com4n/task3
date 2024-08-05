import os
import multiprocessing
import threading
import numpy as np
import time

def process_matrix_file(file_path, output_dir):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    result = []
    for line in lines:
        matrix = np.array(eval(line.strip()))
        processed_matrix = matrix.transpose()  # Example operation
        result.append(processed_matrix)

    output_path = os.path.join(output_dir, os.path.basename(file_path).replace('.in', '.out'))
    with open(output_path, 'w') as file:
        for matrix in result:
            file.write(str(matrix.tolist()) + '\n')

def process_files_in_parallel(input_dir, output_dir, use_multiprocessing=True):
    files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith('.in')]

    if use_multiprocessing:
        with multiprocessing.Pool() as pool:
            pool.starmap(process_matrix_file, [(f, output_dir) for f in files])
    else:
        threads = []
        for f in files:
            thread = threading.Thread(target=process_matrix_file, args=(f, output_dir))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

def process_files_sequentially(input_dir, output_dir):
    files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith('.in')]
    for f in files:
        process_matrix_file(f, output_dir)

if __name__ == "__main__":
    input_dir = './input'
    output_dir = './output'

    os.makedirs(output_dir, exist_ok=True)

    # Sequential processing
    start_time = time.time()
    process_files_sequentially(input_dir, output_dir)
    end_time = time.time()
    print(f"Sequential processing time: {end_time - start_time} seconds")

    # Multiprocessing
    start_time = time.time()
    process_files_in_parallel(input_dir, output_dir, use_multiprocessing=True)
    end_time = time.time()
    print(f"Multiprocessing time: {end_time - start_time} seconds")

    # Multithreading
    start_time = time.time()
    process_files_in_parallel(input_dir, output_dir, use_multiprocessing=False)
    end_time = time.time()
    print(f"Multithreading time: {end_time - start_time} seconds")
