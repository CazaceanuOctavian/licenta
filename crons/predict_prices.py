import subprocess
import configparser

config = configparser.ConfigParser()
config.read('/home/tavi/Desktop/licenta/cfg.ini')

scripts = [config['Scripts']['dataset_builder'], config['Scripts']['model_trainer'], config['Scripts']['prediction_maker']]

for script in scripts:
    print(f'Strating {script}...')

    process = subprocess.run(['python3', script], capture_output=True, text=True)

    if process.returncode == 0:
        print(f'{script} finished succesfully.')
    else:
        print(f'Error running {script} -- OUTPUT: {process.stderr}')
    print('------------------------------------')