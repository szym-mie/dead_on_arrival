from pathlib import Path

from export_common import exec_command, read_script_from_file, get_param, find_files, create_filepath

image_format = '.png'

gimp_exec = get_param(0)

gimp_batches = [""]
files_to_process = 0

for image_in, rel_path in find_files("**/*.xcf", "src/tex/"):
    image_out = Path("tex/").joinpath(rel_path).with_suffix('.png')

    export_script = read_script_from_file(
        "build/src/export.scm",
        {"in": image_in.as_posix(), "out": image_out.as_posix()})

    create_filepath(image_out)
    batch = f" -b \"{export_script}\""
    if len(gimp_batches[-1]) + len(batch) > 8100:
        gimp_batches.append("")

    gimp_batches[-1] += batch
    files_to_process += 1
    print(f"{image_in} -> {image_out}")

print(f"{files_to_process} files to process")
for batch_index, gimp_batch in enumerate(gimp_batches):
    print(f"processed {batch_index} batches out of {len(gimp_batches)}")

    exec_command(f"{gimp_exec} -d -f -i {gimp_batch} -b \"(gimp-quit 0)\"")
