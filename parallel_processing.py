import concurrent.futures

def process_file_parallel(files, options, process_file_function):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(process_file_function, files, [options] * len(files))
    return list(results)
