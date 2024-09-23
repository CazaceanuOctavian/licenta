import subprocess

scripts = [r'../regression/datasetBuilder.py', r'../regression/modelTrainer.py', r'../regression/predictionMaker.py']

for script in scripts:
    print(f'Strating {script}...')

    process = subprocess.run(['python3', script], capture_output=True, text=True)

    if process.returncode == 0:
        print(f'{script} finished succesfully.')
    else:
        print(f'Error running {script} -- OUTPUT: {process.stderr}')
    print('------------------------------------')