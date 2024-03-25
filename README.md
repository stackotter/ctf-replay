# `ctf-replay`

Allows downloading of individual ctfs and challenges from the massive `sajjadium/ctf-archives` repo.

## Usage

```console
$ python3 archivist.py --help                       
usage: manager [-h] [--category CATEGORY] [--challenge CHALLENGE] ctf year

positional arguments:
  ctf
  year

options:
  -h, --help            show this help message and exit
  --category CATEGORY
  --challenge CHALLENGE
```

## Planned

- [ ] Search for challenges matching flexible criteria.
- [ ] Option to automatically host challenges when possible (if they have a `docker-compose.yml`).
- [ ] Option to detect missing flag files and create dummy flags in their place.
- [ ] Interactive command-line archive browser.
