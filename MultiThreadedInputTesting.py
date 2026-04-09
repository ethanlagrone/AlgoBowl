import os
import subprocess
from concurrent.futures import ProcessPoolExecutor

def run_test_case(filename):
    """Function to handle a single test case."""
    input_folder = "Inputs"
    output_folder = "Outputs"
    
    filepath = os.path.join(input_folder, filename)

    if filename.startswith("input"):
        output_filename = "output" + filename[len("input"):]
    else:
        output_filename = filename

    output_path = os.path.join(output_folder, output_filename)

    with open(filepath, "r") as infile:
        result = subprocess.run(
            ["python", "Main.py"],
            stdin=infile,
            capture_output=True,
            text=True
        )

    with open(output_path, "w") as f:
        f.write(result.stdout)
        if result.stderr:
            f.write("\nERRORS:\n" + result.stderr)

    return f"--- {filename} -> {output_filename} ---"

def main():
    input_folder = "Inputs"
    output_folder = "Outputs"
    os.makedirs(output_folder, exist_ok=True)

    files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]

    print(f"Starting execution on {os.cpu_count()} cores...")

    with ProcessPoolExecutor() as executor:
        results = list(executor.map(run_test_case, files))

    for log in results:
        print(log)

if __name__ == "__main__":
    main()