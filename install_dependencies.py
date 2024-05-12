import json
import subprocess

def install_dependencies():
    with open('requirements.json', 'r') as file:
        requirements = json.load(file)
    
    for dependency, version in requirements['dependencies'].items():
        subprocess.run(['pip', 'install', f'{dependency}{version}'])

if __name__ == '__main__':
    install_dependencies()
