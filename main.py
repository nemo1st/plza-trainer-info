#!/usr/bin/env python3
"""
CLI Tool: Save file repair and CoreData retrieval
"""
import sys
from pathlib import Path
from plaza.crypto.swishcrypto import SwishCrypto
from plaza.crypto.hashdb import HashDB
from plaza.types.accessors import HashDBKeys
from plaza.types.coredata import CoreData


def get_core_data(input_path: str):
    """Retrieve CoreData from save file"""

    # Read input file
    input_file = Path(input_path)
    if not input_file.exists():
        print(f"Error: File not found: {input_path}")
        return None

    with open(input_file, 'rb') as f:
        data = f.read()

    # Verify hash
    if not SwishCrypto.get_is_hash_valid(data):
        print("Error: Invalid hash")
        return None

    print("✓ Hash verification successful")

    # Decrypt
    blocks = SwishCrypto.decrypt(data)
    print(f"✓ Decrypted {len(blocks)} blocks")

    # Create HashDB and retrieve CoreData block
    hash_db = HashDB(blocks)

    try:
        core_data_block = hash_db[HashDBKeys.CoreData]
        core_data = CoreData.from_bytes(core_data_block.data)
        print(f"✓ CoreData retrieved: {core_data}")
        return core_data
    except KeyError:
        print("Error: CoreData not found")
        return None


def modify_core_data(input_path: str, output_path: str = None, name: str = None, player_id: str = None):
    """Modify CoreData and save the file"""

    # Read input file
    input_file = Path(input_path)
    if not input_file.exists():
        print(f"Error: File not found: {input_path}")
        return False

    with open(input_file, 'rb') as f:
        data = f.read()

    # Verify hash
    if not SwishCrypto.get_is_hash_valid(data):
        print("Error: Invalid hash")
        return False

    print("✓ Hash verification successful")

    # Decrypt
    blocks = SwishCrypto.decrypt(data)
    print(f"✓ Decrypted {len(blocks)} blocks")

    # Create HashDB and retrieve CoreData block
    hash_db = HashDB(blocks)

    try:
        core_data_block = hash_db[HashDBKeys.CoreData]
        core_data = CoreData.from_bytes(core_data_block.data)
        print(f"✓ Current CoreData: {core_data}")

        # Change name
        if name is not None:
            old_name = core_data.get_name_string()
            core_data.set_name_string(name)
            print(f"✓ Name changed: {old_name} → {name}")

        # Change ID
        if player_id is not None:
            old_id = core_data.id
            core_data.set_id(player_id)
            print(f"✓ ID changed: {old_id} → {core_data.id}")

        # Write modified CoreData back to block
        core_data_block.change_data(core_data.to_bytes())
        print(f"✓ Modified CoreData: {core_data}")

    except KeyError:
        print("Error: CoreData not found")
        return False

    # Re-encrypt
    modified_data = SwishCrypto.encrypt(blocks)
    print("✓ Data re-encrypted")

    # Determine output path
    if output_path is None:
        output_path = str(input_file.parent / f"{input_file.stem}_modified{input_file.suffix}")

    # Save
    with open(output_path, 'wb') as f:
        f.write(modified_data)

    print(f"✓ Saved successfully: {output_path}")
    return True


def repair_save(input_path: str, output_path: str = None):
    """Read save file, repair and save"""

    # Read input file
    input_file = Path(input_path)
    if not input_file.exists():
        print(f"Error: File not found: {input_path}")
        return False

    with open(input_file, 'rb') as f:
        data = f.read()

    # Verify hash
    if not SwishCrypto.get_is_hash_valid(data):
        print("Error: Invalid hash")
        return False

    print("✓ Hash verification successful")

    # Decrypt
    blocks = SwishCrypto.decrypt(data)
    print(f"✓ Decrypted {len(blocks)} blocks")

    # Re-encrypt (repair)
    repaired_data = SwishCrypto.encrypt(blocks)
    print("✓ Data re-encrypted")

    # Determine output path
    if output_path is None:
        output_path = str(input_file.parent / f"{input_file.stem}_repaired{input_file.suffix}")

    # Save
    with open(output_path, 'wb') as f:
        f.write(repaired_data)

    print(f"✓ Repair completed: {output_path}")
    return True


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python main.py <input_file> [output_file]                    - Repair save file")
        print("  python main.py --core-data <input_file>                      - Display CoreData")
        print("  python main.py --modify <input_file> --name <name>           - Change name")
        print("  python main.py --modify <input_file> --id <ID>               - Change ID")
        print("  python main.py --modify <input_file> --name <name> --id <ID> [output_file] - Change name and ID")
        print("")
        print("Examples:")
        print("  python main.py save.bin")
        print("  python main.py save.bin save_fixed.bin")
        print("  python main.py --core-data save.bin")
        print("  python main.py --modify save.bin --name ZA --id 0412898312")
        sys.exit(1)

    # CoreData display mode
    if sys.argv[1] == "--core-data":
        if len(sys.argv) < 3:
            print("Error: Please specify input file")
            sys.exit(1)
        core_data = get_core_data(sys.argv[2])
        if core_data:
            print("\n=== CoreData Details ===")
            print(f"ID: {core_data.id}")
            print(f"Name: {core_data.get_name_string()}")
            print(f"Gender: {core_data.get_gender().name}")
            print(f"Rank: {core_data.member_rank}")
            print(f"Rank EXP: {core_data.member_rank_exp}")
            print(f"Birthday: {core_data.birthday_month}/{core_data.birthday_day}")
            print(f"Eggs Hatched: {core_data.egg_hatch_count}")
            print(f"Partner Walk Count: {core_data.partner_walk_count}")
        sys.exit(0 if core_data else 1)

    # CoreData modification mode
    if sys.argv[1] == "--modify":
        if len(sys.argv) < 3:
            print("Error: Please specify input file")
            sys.exit(1)

        input_path = sys.argv[2]
        name = None
        player_id = None
        output_path = None

        # Parse arguments
        i = 3
        while i < len(sys.argv):
            if sys.argv[i] == "--name" and i + 1 < len(sys.argv):
                name = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--id" and i + 1 < len(sys.argv):
                # Accept as string (preserve leading zeros)
                player_id = sys.argv[i + 1]
                i += 2
            else:
                # Output file path
                if not sys.argv[i].startswith("--"):
                    output_path = sys.argv[i]
                i += 1

        if name is None and player_id is None:
            print("Error: Please specify --name or --id")
            sys.exit(1)

        success = modify_core_data(input_path, output_path, name, player_id)
        sys.exit(0 if success else 1)

    # Repair mode
    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None

    success = repair_save(input_path, output_path)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
