import xml.etree.ElementTree as ET
from collections import defaultdict


def gather_all_categories(types_file):
    tree = ET.parse(types_file)
    root = tree.getroot()
    categories = set()

    for type_elem in root.findall("type"):
        category_elem = type_elem.find("category")
        if category_elem is not None:
            categories.add(category_elem.get("name"))

    return sorted(categories)


def extract_items_with_nominal_zero(types_file, category):
    tree = ET.parse(types_file)
    root = tree.getroot()
    items = []

    for type_elem in root.findall("type"):
        item_name = type_elem.get("name")
        nominal = (
            int(type_elem.find("nominal").text)
            if type_elem.find("nominal") is not None
            else 0
        )
        item_category = (
            type_elem.find("category").get("name")
            if type_elem.find("category") is not None
            else ""
        )

        if nominal == 0 and item_category.lower() == category.lower():
            items.append(item_name)

    return items


def main():
    types_file = "C:/Users/lewis/Documents/GitHub/DayZ-Central-Economy/respawnOffline.charnarusplus/db/types.xml"

    all_categories = gather_all_categories(types_file)
    print("Available categories:")
    for category in all_categories:
        print(f" - {category}")

    chosen_category = input(
        "Enter the category to view items with nominal value of 0: "
    )

    items = extract_items_with_nominal_zero(types_file, chosen_category)

    print(f"Items with nominal value of 0 in category '{chosen_category}':")
    for item in items:
        print(f" - {item}")


if __name__ == "__main__":
    main()
