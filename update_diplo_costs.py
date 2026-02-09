#! /usr/bin/env python

import sys, os
from dotenv import load_dotenv
import re

load_dotenv()

FDIPLOCOST = os.path.join("in_game", "common", "diplomatic_costs", "00_hardcoded.txt")
FINPUT  = os.path.join(os.getenv("EU5_GAME_FOLDER"), FDIPLOCOST)
FOUTPUT = os.path.join(os.getenv("SLURROPA_FOLDER"), FDIPLOCOST)

with open(FINPUT, 'r') as foo:
    diplocosts = foo.read()

# Match only the infiltrate_administration block
block_pattern = re.compile(
    r'(infiltrate_administration\s*=\s*\{)(.*?)(\})',
    re.DOTALL
)

# Match numeric assignments like "spy_network = 50"
number_pattern = re.compile(r'(\s*spy_network\s*=\s*)(-?\d+(?:\.\d+)?)(\s*)')

def replace_value(match):
    prefix, num_str, suffix = match.groups()
    return f"{prefix}999{suffix}"

def process_block(match):
    start, body, end = match.groups()
    new_body = number_pattern.sub(replace_value, body)
    return f"{start}{new_body}{end}"

diplocosts = block_pattern.sub(process_block, diplocosts)


if not os.path.exists(os.path.dirname(FOUTPUT)):
    os.makedirs(os.path.dirname(FOUTPUT))

with open(FOUTPUT, 'w') as foo:
    foo.write(diplocosts)

