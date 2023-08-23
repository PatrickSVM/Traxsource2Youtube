#!/bin/zsh

echo "Update all playlists...\n"

python scripts/deep_house.py
echo "===================================================================\n\n"
sleep 3
python scripts/house.py
echo "===================================================================\n\n"
sleep 3
python scripts/minimal_deeptech.py
echo "===================================================================\n\n"
sleep 3
python scripts/nu_disco_indie_dance.py


# python scripts/afro_latin_brazilian.py
# python scripts/leftfield.py
# python scripts/lounge_chillout.py