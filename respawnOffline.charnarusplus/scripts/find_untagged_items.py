import xml.etree.ElementTree as ET


def find_items_without_element(types_file, element_name):
    tree = ET.parse(types_file)
    root = tree.getroot()
    items = []

    for type_elem in root.findall("type"):
        item_name = type_elem.get("name")
        element = type_elem.find(element_name)
        if element is None:
            items.append(item_name)

    return items


def write_items_to_file(items, filename):
    with open(filename, "w") as file:
        for item in items:
            file.write(f"{item}\n")


def main():
    types_file = "C:/Users/lewis/Documents/GitHub/DayZ-Central-Economy/respawnOffline.charnarusplus/db/types.xml"

    search_option = (
        input("Enter the element to search for (tag or usage): ").strip().lower()
    )
    if search_option not in ["tag", "usage"]:
        print("Invalid option. Please enter 'tag' or 'usage'.")
        return

    items = find_items_without_element(types_file, search_option)

    output_file = f"items_without_{search_option}.txt"
    write_items_to_file(items, output_file)

    print(f"Items without <{search_option}> element have been written to {output_file}")


if __name__ == "__main__":
    main()
