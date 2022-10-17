import subprocess
from pathlib import Path

if __name__ == "__main__":
    token = Path(".pypi-token").read_text().strip()
    cmd = f"poetry publish --build --username __token__ --password {token}"
    subprocess.run(cmd, shell=True)
