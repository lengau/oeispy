"""OEIS data constants."""

import json
import pathlib

DATA_FILE = pathlib.Path(__file__)

a2_json = json.loads(DATA_FILE.with_name("A000002.json").read_text())["results"][0]
