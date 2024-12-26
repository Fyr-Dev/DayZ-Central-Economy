import xml.etree.ElementTree as ET
import re


def standardize_weapon_variants_with_list(input_file, output_file):
    """
    Sets spawn stats of weapon variants to match their base weapons
    for only _black and _green variants (excluding platecarrier, sawedoffmosin, mediumtent, civsedan),
    then prints a list of changed variants.
    """
    tree = ET.parse(input_file)
    root = tree.getroot()

    base_weapons_data = {}
    changed_variants = []

    # Keywords to exclude
    excluded_bases = [
        "platecarrier",
        "sawedoffmosin",
        "mediumtent",
        "civsedan",
        "civiliansedan",
    ]

    # 1. Gather stats from "base" weapons.
    for type_elem in root.findall("type"):
        name = type_elem.get("name")
        if not name:
            continue

        base_name = re.split(r"[_-]", name.lower())[0]

        # Collect stats from base weapons.
        weapon_stats = {}
        for child in type_elem:
            if child.tag in ["nominal", "min", "quantmin", "quantmax"]:
                weapon_stats[child.tag] = child.text

        # If exact match, store the base's stats.
        if name.lower() == base_name:
            base_weapons_data[base_name] = weapon_stats

    # 2. Apply stats only to _black/_green variants, skipping excluded bases.
    for type_elem in root.findall("type"):
        name = type_elem.get("name")
        if not name:
            continue

        if name.lower().endswith("_black") or name.lower().endswith("_green"):
            variant_base = re.split(r"[_-]", name.lower())[0]
            if (
                variant_base in base_weapons_data
                and name.lower() != variant_base
                and not any(ex in variant_base for ex in excluded_bases)
            ):
                base_stats = base_weapons_data[variant_base]
                for child in type_elem:
                    if child.tag in base_stats:
                        child.text = base_stats[child.tag]
                changed_variants.append(name)

    # 3. Write the updated XML and print changed variants.
    tree.write(output_file, encoding="UTF-8", xml_declaration=True)
    print("The following weapon variants had stats changed:\n")
    for variant in changed_variants:
        print(f" - {variant}")


standardize_weapon_variants_with_list(
    "C:/Users/lewis/Documents/GitHub/DayZ-Central-Economy/respawnOffline.charnarusplus/db/types.xml",
    "C:/Users/lewis/Documents/GitHub/DayZ-Central-Economy/respawnOffline.charnarusplus/db/types.xml",
)
