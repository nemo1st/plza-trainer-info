# PLZA Change TrainerInfo
<sub>This project is not associated with TPC (The Pokémon Company), GameFreak, Nintendo nor any other entity.</sub>

---

## Dependencies
- Python 3.13

## How to Use it

```sh
# Repair save file
$ python3 main.py main

## Display CoreData
python3 main.py --core-data main

## Modify name and ID (with leading zeros)
python3 main.py --modify main --name ZA --id 0810123456
```

## Thanks to:
- @azalea-w of [plza-save-utils](https://github.com/azalea-w/plza-save-utils)
- The maintainers of [PKHeX](https://github.com/kwsch/PKHeX/) for implementing SwishCrypto
- GameFreak for creating the game
- @entropiccode for [their exploration of the items](https://github.com/entropiccode/legends_za_item_codes/)
