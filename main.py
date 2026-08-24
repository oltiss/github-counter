import subprocess
import sys
from pathlib import Path

# Ustalenie ścieżki do folderu z projektem
BASE_DIR = Path(__file__).resolve().parent
COUNTER_FILE = BASE_DIR / "counter.txt"

def run_cmd(cmd: list[str]) -> subprocess.CompletedProcess:
    """Pomocnik do bezpiecznego uruchamiania poleceń w katalogu repozytorium."""
    return subprocess.run(
        cmd,
        cwd=BASE_DIR,
        capture_output=True,
        text=True,
        check=True
    )

def increment_counter() -> int:
    count = 0
    if COUNTER_FILE.exists():
        try:
            count = int(COUNTER_FILE.read_text().strip())
        except (ValueError, OSError):
            count = 0

    count += 1
    COUNTER_FILE.write_text(f"{count}\n")
    return count

def git_sync_and_push(count: int):
    try:
        # 1. Pobranie ewentualnych zmian zdalnych
        run_cmd(["git", "pull", "--rebase"])

        # 2. Stage'owanie pliku licznika
        run_cmd(["git", "add", "counter.txt"])

        # 3. Sprawdzenie, czy są zmiany do zatwierdzenia
        diff_check = subprocess.run(
            ["git", "diff", "--staged", "--quiet"],
            cwd=BASE_DIR
        )

        # Kod 1 oznacza, że wystąpiły zmiany do commitowania
        if diff_check.returncode == 1:
            run_cmd(["git", "commit", "-m", f"chore: increment counter to {count} [skip ci]"])
            run_cmd(["git", "push", "origin", "main"])
            print(f"Pomyślnie zaktualizowano licznik do {count} i wykonano git push.")
        else:
            print("Brak zmian do zatwierdzenia w Git.")

    except subprocess.CalledProcessError as e:
        print(f"Błąd operacji Git: {e.stderr.strip()}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    new_count = increment_counter()
    git_sync_and_push(new_count)
