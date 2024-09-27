import subprocess
import configparser
import sys
import time
import datetime

config = configparser.ConfigParser()
config.read('/home/tav/Desktop/licenta/cfg.ini')

currentDate = datetime.datetime.now()
start_time = time.time()
#scrape for 28800 seconds (8 hours) at a time
timeout = 30
last_print_time = 0  


scripts = [config['Scripts']['evomag_scraper'], config['Scripts']['vexio_scraper']]
processes = []

for script in scripts:
        process = subprocess.Popen(['python3', script], stdout=None, stderr=None)
        processes.append(process)

try:
    print(str(currentDate) + ' --> SCRAPING STARTED SUCCESFULLY')
    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time
        if elapsed_time >= timeout:
            print("8 hours have passed! Terminating all processes...")
            break

except KeyboardInterrupt:
    print("\nKeyboardInterrupt detected! Terminating all processes...")

finally:
    for process in processes:
        if process.poll() is None:  
            process.terminate()  
            print(f"Process {process.pid} marked for termination")

    #wait a bit for the processes to write their dying gasp
    time.sleep(2)

    for process in processes:
        try:
            process.wait(timeout=10)
            print(f"Process {process.pid} terminated gracefully.")
        except subprocess.TimeoutExpired:
            print(f"Process {process.pid} did not terminate in time; killing it.")
            process.kill()
            print(f"Process {process.pid} killed.")
        
