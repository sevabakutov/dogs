import os
import sys
import shutil
import platform
import subprocess


def run_command(command, env=None):
    ''' Run command '''
    try:
        subprocess.run(command, check=True, shell=True, env=env)
    except subprocess.CalledProcessError as e:
        print(f"Error: Command {command} failed with exit code {e.returncode}")
        sys.exit(e.returncode)

def create_venv(venv_path):
    ''' Create virtual enviroment '''
    print("Creating virtual enviroment...")
    run_command(f"python -m venv {venv_path}")

def activate_venv(venv_path):
    ''' Activate virtual enviroment '''
    print("Activating virtual enviroment...")
    if platform.system() == "Windows":
        activate_command = os.path.join(venv_path, "Scripts", "activate")
    else:
        activate_command = os.path.join(venv_path, "bin", "activate")
    run_command(activate_command)

# def deactivate_venv():
#     ''' Deactivate virtual enviroment '''
#     print("Deactivating virtual enviroment...")
#     run_command("deactivate")

def install_pyinstaller(venv_path):
    ''' Install pyinstaller '''
    print("Installing pyinstaller...")
    pip_path = os.path.join(venv_path, "Scripts" if platform.system() == "Windows" else "bin", "pip")
    run_command(f"{pip_path} install pyinstaller")

def compile_script(venv_path, script_path):
    ''' Compile dogs to dogs.exe '''
    print("Compiling script...")
    installer_path = os.path.join(venv_path, "Scripts" if platform.system() == "Windows" else "bin", "pyinstaller")
    run_command(f"{installer_path} --onefile {script_path}")

def add_to_path(executable_name):
    ''' Add executable file to PATH '''

    for path in os.environ["PATH"].split(os.pathsep):
        if os.path.isdir(path) and os.access(path, os.W_OK):
            try:
                source_path = os.path.join("dist", executable_name)
                target_path = os.path.join(path, executable_name)
                shutil.copy(source_path, target_path)
                print(f"Файл {executable_name} добавлен в {path}")
                return
            except Exception as e:
                print(f"Ошибка при копировании: {e}")
    print("Нет подходящей папки для записи в PATH. Добавьте файл вручную.")



def main():
    venv_path = "venv"
    script_path = os.path.join("..", "dogs.py")
    executable_name = "dogs.exe" if platform.system() == "Windows" else "dogs"

    create_venv(venv_path)
    activate_venv(venv_path)

    install_pyinstaller(venv_path)
    compile_script(venv_path, script_path)

    add_to_path(executable_name)

if __name__ == "__main__":
    main()