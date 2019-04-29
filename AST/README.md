# AST

Parse code snippets into an AST before comparing, analagous to comparing amino acid sequences rather than base pair sequences.

## BabelFish

Using [BabelFish](https://github.com/bblfsh/bblfshd)

On Mac, running Docker Desktop:

```bash

# run bblfshd
docker run -d --name bblfshd --privileged -p 9432:9432 -v bblfsh-storage:/var/lib/bblfshd bblfsh/bblfshd

# install drivers
docker exec -it bblfshd bblfshctl driver install --all

# parse
docker exec -it bblfshd bblfshctl parse /opt/bblfsh/etc/examples/python.py
```
