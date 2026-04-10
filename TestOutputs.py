#Script to test output test cases(probably not functional yet)
import os
import subprocess

input_folder = "outputs"

for filename in os.listdir(input_folder):
    filepath = os.path.join(input_folder, filename)
    print(f"--- {filename} ---")
    result = subprocess.run(["python", "Validater.py"], stdin=open(filepath), capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("ERRORS:", result.stderr)