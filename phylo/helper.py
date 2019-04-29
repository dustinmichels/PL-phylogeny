import json
import textwrap
from IPython.display import display, Markdown, Latex

with open('snippets/fcn_declaration.json') as f:
    fcns = json.load(f)

for k, v in fcns.items():
    txt = f"""
{k}
```{k}
{v}
```
---
"""
    display(Markdown(txt))
