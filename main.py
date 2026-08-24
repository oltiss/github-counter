from pathlib import Path

COUNTER_FILE = Path("counter.txt")


def increment():
    count = 0
    if COUNTER_FILE.exists():
        try:
            count = int(COUNTER_FILE.read_text().strip())
        except (ValueError, OSError):
            count = 0

    count += 1
    COUNTER_FILE.write_text(f"{count}\n")
    print(f"Licznik zaktualizowany do: {count}")


if __name__ == "__main__":
    increment()
