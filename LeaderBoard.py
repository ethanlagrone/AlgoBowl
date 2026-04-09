import os
import re
import shutil

dir1 = "CurrentSubmissions"
dir2 = "Outputs"

def parse_score(filepath):
    with open(filepath, 'r') as f:
        first_line = f.readline().strip()
    match = re.search(r'\d+', first_line)
    if match:
        return int(match.group())
    return -1  # invalid or missing score

def build_leaderboard(dir1, dir2, leaderboard_dir):
    os.makedirs(leaderboard_dir, exist_ok=True)

    files1 = set(os.listdir(dir1))
    files2 = set(os.listdir(dir2))
    all_files = files1 | files2

    for filename in all_files:
        path1 = os.path.join(dir1, filename) if filename in files1 else None
        path2 = os.path.join(dir2, filename) if filename in files2 else None

        # Only exists in one dir
        if path1 and not path2:
            winner = path1
        elif path2 and not path1:
            winner = path2
        else:
            # Exists in both — compare scores
            score1 = parse_score(path1)
            score2 = parse_score(path2)

            if score1 == -1 and score2 == -1:
                continue  # both invalid, skip
            elif score1 >= score2:
                winner = path1
            else:
                winner = path2

        shutil.copy2(winner, os.path.join(leaderboard_dir, filename))
        print(f"{filename}: copied from {winner}")

if __name__ == "__main__":
    build_leaderboard(dir1, dir2, "leaderboard")