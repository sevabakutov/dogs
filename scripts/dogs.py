import sys
import subprocess

DOCKER_NAME = "dogs-cli"
ENV_FILE = "../ml_project/.secret/.env"
SHARED_DIR = "../ml_project/data/results:/usr/src/ml_project/ml_project/data/results"

def main():
    if len(sys.argv) < 2:
        print("Usage: dogs <command> [args...]")
        sys.exit(1)
    
    command = [
        "docker", "run", "--rm",
        "--env-file", ENV_FILE,
        "-v", SHARED_DIR,
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