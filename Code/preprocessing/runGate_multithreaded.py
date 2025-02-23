import psutil
import subprocess
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from timer_deco import timer

@timer
def get_system_resources(output_location):
    num_cpus = psutil.cpu_count(logical=True)
    total_memory = psutil.virtual_memory().available
    total_disk = psutil.disk_usage(output_location).free 
    return num_cpus, total_memory, total_disk

#############################################################
# define your custom shell command in this function         #
#############################################################
@timer
def run_gate_with_setup(macro_file, output_location):
    # define custom shell command
    command = f"""
    pwd >> {output_location}/{macro_file.stem}.log
    source /home/alex/.bashrc
    Gate {macro_file} >> {output_location}/{macro_file.stem}.log
    """
    try:
        # Run the custom shell command with bash 
        proc = subprocess.Popen(command, shell=True, executable='/bin/bash')
        print(f"Gate started with macro file: {macro_file}")

        # Give the shell some time to spawn the GATE process
        time.sleep(5)

        # Get the child process (should be GATE)
        proc_info = psutil.Process(proc.pid)
        gate_processes = proc_info.children()

        # Ensure that the GATE process and not the shell is monitored 
        if len(gate_processes) == 0:
            print("No child processes found, GATE might not have started yet.")
            return None
        gate_proc = gate_processes[0]  # Assuming GATE is the first child process
        print(f"GATE process found with PID: {gate_proc.pid}")

        return gate_proc
    except FileNotFoundError:
        print("Failed to run Gate.")
        return None
    except Exception as e:
        print(f"Failed to run Gate: {e}")
        return None

@timer
def check_gate_ram_usage(proc):
    try:
        proc_info = psutil.Process(proc.pid)
        ram_usage = proc_info.memory_info().rss
        cpu_usage = proc_info.cpu_percent(interval=1)
        print(f"Gate is using {ram_usage / (1024 ** 2):.2f} MB of RAM and {cpu_usage:.2f}% of a single CPU core.")
        return ram_usage, cpu_usage
    except psutil.NoSuchProcess:
        print("The Gate process is no longer running.")
        return 0, 0
    except Exception as e:
        print(f"An error occurred while checking the RAM usage: {e}")
        return 0, 0


@timer
def check_gate_peak_usage(proc, wait_time=45, check_interval=5, stable_threshold=3):
    peak_cpu_usage = 0
    stable_ram_usage = 0
    stable_count = 0
    try:
        proc_info = psutil.Process(proc.pid)
        
        # Wait for the initial setup to complete
        print(f"Waiting {wait_time} seconds for the process to stabilize...")
        time.sleep(wait_time)

        while proc.is_running():
            # RAM usage in bytes
            ram_usage = proc_info.memory_info().rss 
            # CPU percent over 1 (-> argument) second
            cpu_usage = proc_info.cpu_percent(interval=1) 

            # Track peak CPU usage
            if cpu_usage > peak_cpu_usage:
                peak_cpu_usage = cpu_usage

            # Check for RAM stability (change fluctuation threshold, if necessary)
            if stable_ram_usage == 0 or abs(ram_usage - stable_ram_usage) < (5 * 1024 ** 2):  
                stable_ram_usage = ram_usage
                stable_count += 1
            else:
                stable_count = 0

            # If RAM has been stable for enough checks, we assume it's the stable value
            if stable_count >= stable_threshold:
                break

            time.sleep(check_interval)

        print(f"Peak CPU Usage: {peak_cpu_usage:.2f}%")
        print(f"Stable RAM Usage: {stable_ram_usage / (1024 ** 2):.2f} MB")

        return stable_ram_usage, peak_cpu_usage

    except psutil.NoSuchProcess:
        print("The process is no longer running.")
        return 0, 0
    except Exception as e:
        print(f"An error occurred while checking the process usage: {e}")
        return 0, 0

@timer
def run_macro(macro_file, output_location):
    start_time = time.time()  
    proc = run_gate_with_setup(macro_file, output_location)
    if proc is None:
        raise Exception(f"Failed to run Gate with macro file: {macro_file}")
    while proc.is_running():
        time.sleep(10)
    end_time = time.time()  
    elapsed_time = end_time - start_time
    log_message = f"run_macro with {macro_file}' took {elapsed_time:.4f} seconds to execute.\n"
    with open("logs/timetest.log", "a") as logfile:
        logfile.write(log_message)
    return proc

@timer
def manage_Gate_processes_m(output_location, cores, ram):
    try:
        num_cpus, total_memory, total_disk = get_system_resources(output_location)
    except Exception as e:
        raise Exception(f"An error occurred while getting system resources: {e}")
    if cores > num_cpus:
        raise Exception("Number of cores requested exceeds the number of CPUs.")
    if ram*(1024**2) > total_memory:
        raise Exception("Requested RAM exceeds total memory.")

    if not Path(output_location).is_dir():
        raise Exception("Invalid output location.")

    try:
        macro_files = list(Path(output_location).glob('macros/*.mac'))
        # Sorting function: Extract numeric part and use it as the sorting key
        macro_files = sorted(macro_files, key=lambda p: int(p.stem.split('_')[-1]))
        print(macro_files)
    except Exception as e:
        raise Exception(f"An error occurred while reading the macro files: {e}")

    if len(macro_files) == 0:
        raise Exception("No macro files found.")

    start_time = time.time()
    first_proc = run_gate_with_setup(macro_files[0], output_location)
    if first_proc is None:
        raise Exception("Failed to run Gate with the first macro.")
    print("First macro started")

    if first_proc.is_running():
        # not used in this version
        ## ram_usage, cpu_usage = check_gate_ram_usage(first_proc)
        # Check the RAM usage of the GATE process (CPU possible, if the use case requires it)
        ram_usage, cpu_usage = check_gate_peak_usage(first_proc)
    else:
        raise Exception("Gate process exited unexpectedly or too early to measure. Consider changing the sleep time")

    max_processes = int(ram*(1024 ** 2)/ ram_usage)
    print("Max processes per RAM:" + str(max_processes))
    if max_processes > cores:
        max_processes = cores
    print("Max processes:" + str(max_processes))
    try:
        first_proc.terminate()  # Attempt graceful shutdown
        first_proc.wait(timeout=5)  # Wait for up to 5 seconds for it to exit
    except subprocess.TimeoutExpired:
        print("Process did not terminate in time. Forcing kill.")
        first_proc.kill()  # Forcefully kill the process
    except Exception as e:
        print(f"An error occurred while killing the process: {e}")


    storage = False

    start_time = time.time()
    with ThreadPoolExecutor(max_workers=max_processes) as executor:
        future_to_macro = {executor.submit(run_macro, macro_file, output_location): macro_file for macro_file in macro_files}

        for future in as_completed(future_to_macro):
            macro_file = future_to_macro[future]
            try:
                proc = future.result() 

                print(f"Macro file {macro_file} finished.")

                if macro_file == macro_files[0] and not storage:
                    storage = sum(f.stat().st_size for f in Path(output_location).glob('split_0/*') if f.is_file())
                    end_time = time.time()
                    print(f"First macro finished in approximately {end_time - start_time:.2f} seconds and produced {storage / (1024 ** 2):.2f} MB of data.")
                    
                    if storage * len(macro_files) > total_disk:
                        print("Warning: The total output size will likely exceed the free disk space.")
                        
            except Exception as exc:
                print(f"Macro file {macro_file} generated an exception: {exc}")

    # handle the case of waiting for the first macro to finish
    while first_proc.is_running():
        time.sleep(5)
