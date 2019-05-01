import os
import json
import textwrap


def prepare_snippets(root_dir: str):
    """Update JSON files with code snippets in code folders"""

    # load mapping of extensions to language names
    extensions = load_extensions(root_dir)

    # load list of dirs in root_folder, filter out auto-generated folders
    dirs = [x for x in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, x))]
    dirs = [x for x in dirs if x[0] not in [".", "_"]]

    # update data (JSON) files in each code dir
    for d in dirs:
        code_dir = os.path.join(root_dir, d)
        _process_code_files(code_dir, extensions)


def load_extensions(root_dir: str) -> dict:
    """Load dict mapping file extensions to language names"""
    fp = os.path.join(root_dir, "ext.json")
    with open(fp) as f:
        return json.load(f)


def _process_code_files(code_dir: str, extensions: dict):
    """Given a dir with code snippets (in src) consolidate data into single JSON"""
    src_dir = os.path.join(code_dir, "src")
    out_dir = os.path.join(code_dir, "out")

    # code snippets into single data dict
    data_dict = _code_into_dict(src_dir, extensions)
    dict_outfile = os.path.join(out_dir, "data.json")
    print(f"    {src_dir} => {dict_outfile}")
    with open(dict_outfile, "w") as f:
        json.dump(data_dict, f, indent=2)

    # code snippets into markdown string
    md = _data_into_md(data_dict)
    md_outfile = os.path.join(out_dir, "snippets.md")
    print(f"    {src_dir} => {md_outfile}")
    with open(md_outfile, "w") as f:
        f.write(md)


def _code_into_dict(src_dir: str, extensions: dict) -> dict:
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


def _data_into_md(data_dict: dict) -> str:
    """Given dict with <lang: code> data, create markdown string repr"""
    md = ""
    for lang in sorted(data_dict):
        code = data_dict[lang]
        # lang_shortname = lang.split(" ")[-1]  # ie, "common lisp -> lisp"
        lang_shortname = lang.replace(" ", "")  # remove spaces
        md += f"**{lang_shortname}**\n\n```{lang_shortname}\n{code}\n```\n\n----\n\n"
    return md


if __name__ == "__main__":
    print("Processing code snippets into consolidated formats...")
    prepare_snippets("code_snippets")
    print("Done")
