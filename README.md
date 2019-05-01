# Language Phylo

Phylogenetic tree of programming languages constructed from code snippets

> STATUS: Early! In progress.

![Early Tree](notebooks/tree.png)

## Setup

```bash
# create conda env
conda env create -f environment.yml

# activate
conda activate phylo

# install dev dependencies
pip install -r dev-requirements.txt
```

Alternatively...

```bash
conda env create -f full_env.yml
```

Also helpful:

```bash
# remove environemt
conda remove --name phylo --all

# export env to file
conda env export > full_env.yml
```
