# NYT Sudoku → OpenSudoku Exporter

This project fetches the daily **New York Times Sudoku** puzzles and converts them into the **OpenSudoku** import format.

The script automatically:

- Downloads the daily puzzles (easy, medium,hard)
- Converts them to `.opensudoku` XML collections
- Appends puzzles
grouped by difficulty
- Runs cleanly inside a Docker container for automation

------------------------------------------------------------------------

## Project Structure

    .
    ├─ main.py
    ├─ fetch_nyt.py
    ├─ append_to_opensudoku.py
    ├─ requirements.txt
    ├─ Dockerfile
    ├─ docker-compose.yml
    └─ nyt_opensudoku/

Output files are written into:

    nyt_opensudoku/

One file per difficulty:

- `nyt_easy.opensudoku`
- `nyt_medium.opensudoku`
- `nyt_hard.opensudoku`

------------------------------------------------------------------------

## Running Locally

Install dependencies:

``` bash
pip install -r requirements.txt
```

Run:

``` bash
python main.py
```

------------------------------------------------------------------------

## Running with Docker

Build the container:

``` bash
docker compose build
```

Run once:

``` bash
docker compose run --rm nyt-sudoku
```

The exported files will appear in:

    ./nyt_opensudoku

------------------------------------------------------------------------

## Automation with Cron (Recommended)

Because the container runs once and exits, it is ideal for scheduling
with cron.

Edit your crontab:

``` bash
crontab -e
```

Example: run every day at 06:00

``` bash
0 6 * * * cd /absolute/path/to/nyt-sudoku-exporter && /usr/bin/docker compose run --rm nyt-sudoku >> cron.log 2>&1
```

Notes:

- Replace the path with your project directory.
- Use `which docker` if the docker path differs.
- Output is written to `cron.log` for debugging.

------------------------------------------------------------------------

## License

Personal project for experimentation and automation.
