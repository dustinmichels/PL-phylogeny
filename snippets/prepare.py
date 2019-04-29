import os
import json


def prepare_snippets(root_dir):
    """Update JSON files with code snippets in code folders"""

    # load mapping of extensions to language names
    extensions = _load_extensions(root_dir)

    # load list of dirs in root_folder
    dirs = [x for x in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, x))]

    # update data (JSON) files in each code dir
    for d in dirs:
        code_dir = os.path.join(root_dir, d)
        _consolidate_code_files(code_dir, extensions)


def _load_extensions(root_dir):
    """Load dict mapping file extensions to language names"""
    fp = os.path.join(root_dir, "ext.json")
    with open(fp) as f:
        return json.load(f)


def _consolidate_code_files(code_dir, extensions):
    """Given a dir with code snippets (in src) consolidate data into single JSON"""
    src_dir = os.path.join(code_dir, "src")
    data_dict = _code_into_dict(src_dir, extensions)

    outfile_path = os.path.join(code_dir, "data.json")
    with open(outfile_path, "w") as f:
        json.dump(data_dict, f, indent=2)


def _code_into_dict(src_dir, extensions):
    """Reads code snippets into single dict"""
    data = {}
    files = os.listdir(src_dir)
    for filename in files:
        path = os.path.join(src_dir, filename)
        ext = filename.split(".")[1]
        lang = extensions[ext]
        with open(path) as f:
            code = f.read().strip()
            data[lang] = code
    return data


if __name__ == "main":
    print("preparing code snippets...")
    prepare_snippets(os.curdir)
