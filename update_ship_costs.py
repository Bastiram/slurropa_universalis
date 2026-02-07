#! /usr/bin/env python

import sys, os
from dotenv import load_dotenv
import re

load_dotenv()

FNAVYDEMANDS = os.path.join("in_game", "common", "goods_demand", "navy_demands.txt")
FINPUT  = os.path.join(os.getenv("EU5_GAME_FOLDER"), FNAVYDEMANDS)
FOUTPUT = os.path.join(os.getenv("SLURROPA_FOLDER"), FNAVYDEMANDS)

with open(FINPUT, 'r') as foo:
    navydemands = foo.read()


# Only match these block names
allowed_blocks = (
    r"heavy_ship_[1-6]_construction",
    r"ship_of_the_line_construction"
)
block_name_pattern = r"(?:%s)" % "|".join(allowed_blocks)

# Capture only the desired blocks
block_pattern = re.compile(
    rf"({block_name_pattern}\s*=\s*\{{)(.*?)(\}})",
    re.DOTALL
)

# Match numeric assignments like "key = 1.23"
number_pattern = re.compile(r'(\s*\w+\s*=\s*)(-?\d+(?:\.\d+)?)(\s*)')

def double_number(match):
    prefix, num_str, suffix = match.groups()
    doubled = float(num_str) * 2
    # Keep integers clean
    if doubled.is_integer():
        doubled = f"{doubled:.1f}" # force ".0"
    return f"{prefix}{doubled}{suffix}"

def process_block(match):
    start, body, end = match.groups()
    new_body = number_pattern.sub(double_number, body)
    return f"{start}{new_body}{end}"

navydemands = block_pattern.sub(process_block, navydemands)

if not os.path.exists(os.path.dirname(FOUTPUT)):
    os.makedirs(os.path.dirname(FOUTPUT))

with open(FOUTPUT, 'w') as foo:
    foo.write(navydemands)

