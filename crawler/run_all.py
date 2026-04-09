import subprocess
from pathlib import Path

base_path = Path(__file__).resolve().parent

scripts = [
    "fetch_deals.py",
    "api_fetch.py",
    "merge_deals.py"
]

for script in scripts:
    print(f"실행 중: {script}")
    subprocess.run(["python", str(base_path / script)], check=False)

print("전체 자동 실행 완료")