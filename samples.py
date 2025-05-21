import os
import shutil

samples_dir = "samples"
dump_dir = "samples_release"
os.makedirs(dump_dir, exist_ok=True)

for folder in os.listdir(samples_dir):

    if not os.path.isdir(os.path.join(samples_dir, folder)):
        continue

    for audiofile in os.listdir(os.path.join(samples_dir, folder)):
        source_path = os.path.join(samples_dir, folder, audiofile)
        dest_path = os.path.join(dump_dir, f"{folder[4:]}_{audiofile}")
        shutil.copy2(source_path, dest_path)
