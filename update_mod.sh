#! /usr/bin/env bash

source .env

yes | cp -a game/* "${SLURROPA_FOLDER}/."

for foo in *.py
do
  python $foo
done

