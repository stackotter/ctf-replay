# ctf-replay

Allows downloading of individual ctfs and challenges from the massive `sajjadium/ctf-archives` repo.

## Dependencies

```
pip3 install -r requirements.txt
```

## Usage

```
usage: archivist.py [-h] [--category CATEGORY] [--challenge CHALLENGE] [-m {skip,overwrite,backup,prompt}] ctf year

positional arguments:
  ctf
  year

options:
  -h, --help            show this help message and exit
  --category CATEGORY
  --challenge CHALLENGE
  -m {skip,overwrite,backup,prompt}, --mode {skip,overwrite,backup,prompt}
                        
                                                    skip(default): skip existing files, 
                                                    overwrite: overwrite existing files, 
                                                    backup: backup existing files, 
                                                    prompt: prompt for each file
```

## Planned

- [ ] Search for challenges matching flexible criteria.
- [ ] Option to automatically host challenges when possible (if they have a `docker-compose.yml`).
- [ ] Option to detect missing flag files and create dummy flags in their place.
- [ ] Interactive command-line archive browser.
