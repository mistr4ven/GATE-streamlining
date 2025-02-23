import time

# Decorator to log the time taken by a function to execute used for benchmarking
def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()  
        result = func(*args, **kwargs)
        end_time = time.time()  
        elapsed_time = end_time - start_time
        log_message = f"Function '{func.__name__}' took {elapsed_time:.4f} seconds to execute.\n"
        with open("logs/timetest.log", "a") as logfile:
            logfile.write(log_message)
        return result
    return wrapper
