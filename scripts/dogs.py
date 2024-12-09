import sys
import subprocess

DOCKER_NAME = "dogs-cli"
DOCKER_NETWORK = "dogs_dogs-net"

def main():
    if len(sys.argv) < 2:
        print("Usage: dogs <command> [args...]")
        sys.exit(1)
    
    command = [
        "docker", "run", "--rm",
        "--network", DOCKER_NETWORK,
        DOCKER_NAME, "dogs"
    ] + sys.argv[1:]

    try:
        subprocess.run(command, check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"Error: Command failed with exit code {e.returncode}")
        sys.exit(e.returncode)


if __name__ == "__main__":
    main()