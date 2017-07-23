"""OEIS data constants."""
import json
import pathlib

DATA_FILE = pathlib.Path(__file__)

with DATA_FILE.with_name('A000002.json').open() as f:
    a2_json = json.load(f)['results'][0]
