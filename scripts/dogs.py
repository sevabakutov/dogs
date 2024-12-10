import os
import sys
import subprocess

DOCKER_NAME = "dogs-cli"
ENV_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ml_project', '.secret', '.env')
SHARED_DIR_LOCAL = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ml_project', 'data', 'results')
SHARED_DIR_DOCKER = "/usr/src/ml_project/ml_project/data/results"
SHARED_DIR_PATH = f"{SHARED_DIR_LOCAL}:{SHARED_DIR_DOCKER}"

def main():
    if len(sys.argv) < 2:
        print("Usage: dogs <command> [args...]")
        sys.exit(1)
    
    command = [
        "docker", "run", "--rm",
        "--env-file", ENV_FILE,
        "-v", SHARED_DIR_PATH,
        DOCKER_NAME, "dogs"
    ] + sys.argv[1:]

    try:
        print("Running command:", " ".join(command))
        subprocess.run(command, check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"Error: Command failed with exit code {e.returncode}")
        sys.exit(e.returncode)


if __name__ == "__main__":
    main()