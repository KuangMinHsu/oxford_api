from oxford_api import process, logger
import sys


if __name__ == "__main__":
    logger.set_logger()
    if len(sys.argv) != 2:
        print("python start.py [filename]")
        sys.exit(0)
    filename = sys.argv[1]
    print(f"process {filename}")
    process.process(filename)
