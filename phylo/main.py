import os
import json
from IPython.display import display, Markdown, Latex


def load_snippets_data(name="mult"):
    package_directory = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(
        package_directory, "..", "code_snippets", name, "out", "data.json"
    )
    with open(data_path) as f:
        data = json.load(f)
    return data


def load_snippets_md(name="mult"):
    package_directory = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(
        package_directory, "..", "code_snippets", name, "out", "snippets.md"
    )
    with open(data_path) as f:
        md = f.read()
    return md


def code_to_markdown(lang1: str, lang2: str, data_dict: dict, display=False) -> str:
    """Given dict with <lang: code> data, create markdown string repr"""
    md = ""
    for lang in [lang1, lang2]:
        code = data_dict[lang]
        md += f"**{lang}**\n\n```{lang}\n{code}\n```\n\n----\n\n"
    if display:
        display(Markdown(md))
    return md
