import subprocess
from pathlib import Path

project_path = Path(__file__).resolve().parent.parent

commands = [
    ["git", "add", "."],
    ["git", "commit", "-m", "auto update deals"],
    ["git", "push"]
]

for command in commands:
    print("실행:", " ".join(command))
    subprocess.run(command, cwd=project_path, check=False)

print("Git 자동 반영 완료")