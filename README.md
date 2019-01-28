# Data playback

``` bash
pipenv install                  # Install all packages from Pipfile.
pipenv shell                    # Activate the virtual environment.
```

## Data indexed by milliseconds

``` bash
python playback-ws.py --time_format ms --data data.csv
```

## Data indexed by timestamps

``` bash
python playback-ws.py --time_format ts --data data.csv
```
