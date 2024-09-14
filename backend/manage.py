import sys
from uvicorn import run
from create_table import migrate


def start():
    run("core:app", host="127.0.0.2", port=8005, reload=True)

def main():
    if len(sys.argv) < 2:
        print("Usage: manage.py start")
        sys.exit(1)

    command = sys.argv[1]
    if command == "start":
        start()

    if command == "migrate":
        migrate()

    else:
        print(f"Unknown command {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()