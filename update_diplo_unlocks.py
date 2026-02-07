#! /usr/bin/env python

import sys, os
from dotenv import load_dotenv
import re

load_dotenv()

FUNLOCKS = os.path.join("in_game", "common", "advances", "diplomacy_unlocks.txt")
FINPUT  = os.path.join(os.getenv("EU5_GAME_FOLDER"), FUNLOCKS)
FOUTPUT = os.path.join(os.getenv("SLURROPA_FOLDER"), FUNLOCKS)

with open(FINPUT, 'r') as foo:
    unlocks = foo.read()

# Match only the infiltrate_administration_advance block
block_pattern = re.compile(
    r'(infiltrate_administration_advance\s*=\s*\{)'   # block start
    r'((?:[^{}]|\{[^{}]*\})*)'                        # allow inner {...}
    r'(\})',                                          # final closing brace
    re.DOTALL
)

# Match the age assignment inside the block
age_pattern = re.compile(r'(^\s*age\s*=\s*)age_2_renaissance\b', re.MULTILINE)
req_pattern = re.compile(r'(^\s*requires\s*=\s*)spy_construction_renaissance\b', re.MULTILINE)

def process_block(match):
    start, body, end = match.groups()
    body = age_pattern.sub(r'\1age_3_discovery', body)
    body = req_pattern.sub(r'\1diplomatic_training', body)
    return f"{start}{body}{end}"

unlocks = block_pattern.sub(process_block, unlocks)
unlocks = re.sub(
    r'unlock_diplomacy\s*=\s*\{\s*infiltrate_administration\s*\}',
    r'unlock_country_interaction = slurropa_infiltrate_administration',
    unlocks
)

if not os.path.exists(os.path.dirname(FOUTPUT)):
    os.makedirs(os.path.dirname(FOUTPUT))

with open(FOUTPUT, 'w') as foo:
    foo.write(unlocks)

