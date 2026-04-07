#Script to test input test cases
import os
import subprocess

input_folder = "Inputs"
output_folder = "Outputs"
os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    filepath = os.path.join(input_folder, filename)

    # Rename input* -> output*
    if filename.startswith("input"):
        output_filename = "output" + filename[len("input"):]
    else:
        output_filename = filename

    output_path = os.path.join(output_folder, output_filename)

    result = subprocess.run(
        ["python", "Main.py"],
        stdin=open(filepath),
        capture_output=True,
        text=True
    )

    with open(output_path, "w") as f:
        f.write(result.stdout)
        if result.stderr:
            f.write("\nERRORS:\n" + result.stderr)

    print(f"--- {filename} -> {output_filename} ---")