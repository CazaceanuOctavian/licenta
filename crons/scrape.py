import subprocess
import configparser
import sys

config = configparser.ConfigParser()
config.read('/home/tavi/Desktop/licenta/cfg.ini')

scripts = [config['Scripts']['evomag_scraper'], config['Scripts']['vexio_scraper']]
processes = []

for script in scripts:
        process = subprocess.Popen(['python3', script], stdout=None, stderr=None)
        processes.append(process)

try:
    for process in processes:
        # while True:
        #     console_output = process.stdout.readline()
        #     if console_output:
        #         print(f"Output: {console_output.strip()}")    
        stdout, stderr = process.communicate()  
        print(f"Output: {stdout.decode()}")
        if stderr:
            print(f"Error: {stderr.decode()}")
    sys.exit(1)
except KeyboardInterrupt:
    print("\nKeyboardInterrupt detected! Terminating all processes...")
    for process in processes:
        if process.poll() is None:  
            process.kill()  
            print(f"Process {process.pid} killed.")
