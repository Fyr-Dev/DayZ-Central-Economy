import xml.etree.ElementTree as ET


def boost_military_clothing(xml_file, boost_percent):
    parser = ET.XMLParser(target=ET.TreeBuilder(insert_comments=True))
    tree = ET.parse(xml_file, parser=parser)
    root = tree.getroot()

    boosted_items = []
    military_tag = "military"

    for type_elem in root.findall("type"):
        # Check if it's clothing
        category = type_elem.find("category")
        if category is not None and category.get("name") == "clothes":
            name = type_elem.get("name")
            nominal = type_elem.find("nominal")
            min_elem = type_elem.find("min")
            usages = type_elem.findall("usage")

            # Check if any usage is military-related
            has_military_tag = any(
                usage.get("name", "").lower() == military_tag for usage in usages
            )

            if nominal is not None and has_military_tag:
                old_nominal = int(nominal.text)
                old_min = int(min_elem.text) if min_elem is not None else 0

                # Calculate boosted values
                new_nominal = int(old_nominal * (1 + boost_percent / 100))
                new_min = (
                    int(old_min * (1 + boost_percent / 100))
                    if min_elem is not None
                    else 0
                )

                # Update values
                nominal.text = str(new_nominal)
                if min_elem is not None:
                    min_elem.text = str(new_min)

                boosted_items.append(
                    {
                        "name": name,
                        "old_nominal": old_nominal,
                        "new_nominal": new_nominal,
                        "old_min": old_min,
                        "new_min": new_min,
                    }
                )

    tree.write(xml_file, encoding="utf-8", xml_declaration=True)
    return boosted_items


if __name__ == "__main__":
    xml_file = "C:/Users/lewis/Documents/GitHub/DayZ-Central-Economy/respawnOffline.charnarusplus/db/types.xml"

    # Ask for boost percentage
    while True:
        try:
            boost_percent = float(input("Enter boost percentage (1-100): "))
            if 1 <= boost_percent <= 100:
                break
            else:
                print("Please enter a number between 1 and 100")
        except ValueError:
            print("Please enter a valid number")

    boosted = boost_military_clothing(xml_file, boost_percent)

    print(f"\nBoosted military clothing spawns (increased by {boost_percent}%):")
    for item in boosted:
        print(f"- {item['name']}:")
        print(f"  Nominal: {item['old_nominal']} → {item['new_nominal']}")
        print(f"  Min: {item['old_min']} → {item['new_min']}")
