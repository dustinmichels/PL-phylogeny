import os
import json


def load_snippets_data(name="mult"):
    package_directory = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(
        package_directory, "..", "snippets", name, "out", "data.json"
    )
    with open(data_path) as f:
        data = json.load(f)
    return data


def load_snippets_md(name="mult"):
    package_directory = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(
        package_directory, "..", "snippets", name, "out", "snippets.md"
    )
    with open(data_path) as f:
        md = f.read()
    return md

