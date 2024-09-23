import subprocess
import configparser
import sys

config = configparser.ConfigParser()
config.read('/home/tavi/Desktop/licenta/cfg.ini')

scripts = [config['Scripts']['evomag_scraper'], config['Scripts']['vexio_scraper']]
processes = []

for script in scripts:
        process = subprocess.Popen(['python3', script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        processes.append(process)

try:
    for process in processes:
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
