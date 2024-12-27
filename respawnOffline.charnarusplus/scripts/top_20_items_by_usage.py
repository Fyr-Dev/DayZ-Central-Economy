import xml.etree.ElementTree as ET
from collections import defaultdict


def extract_item_data(types_file, usage_name):
    tree = ET.parse(types_file)
    root = tree.getroot()
    item_data = []

    for type_elem in root.findall("type"):
        item_name = type_elem.get("name")
        nominal = (
            int(type_elem.find("nominal").text)
            if type_elem.find("nominal") is not None
            else 0
        )
        usages = [usage.get("name") for usage in type_elem.findall("usage")]

        if usage_name.lower() in [usage.lower() for usage in usages]:
            item_data.append({"name": item_name, "nominal": nominal, "usages": usages})

    print(f"Found {len(item_data)} items with usage '{usage_name}'")
    return item_data


def count_spawn_points(mapgroupproto_file):
    tree_proto = ET.parse(mapgroupproto_file)
    root_proto = tree_proto.getroot()
    usage_spawn_points = defaultdict(int)

    for group in root_proto.findall("group"):
        usage_elems = group.findall("usage")
        for usage_elem in usage_elems:
            usage_attr = usage_elem.get("name")
            if usage_attr:
                for container in group.findall("container"):
                    spawn_points = len(container.findall("point"))
                    usage_spawn_points[usage_attr] += spawn_points

    return usage_spawn_points


def calculate_average_likelihood(item_data, usage_spawn_points):
    item_likelihood = []
    for item in item_data:
        total_spawn_points = sum(usage_spawn_points[usage] for usage in item["usages"])
        if total_spawn_points > 0:
            average_likelihood = (item["nominal"] / total_spawn_points) * 10
            item_likelihood.append((item["name"], average_likelihood))

    item_likelihood.sort(key=lambda x: x[1], reverse=True)
    return item_likelihood[:20]


def main():
    types_file = "C:/Users/lewis/Documents/GitHub/DayZ-Central-Economy/respawnOffline.charnarusplus/db/types.xml"
    mapgroupproto_file = "C:/Users/lewis/Documents/GitHub/DayZ-Central-Economy/respawnOffline.charnarusplus/mapgroupproto.xml"

    usage_name = input("Enter the usage name to search for: ")

    item_data = extract_item_data(types_file, usage_name)
    usage_spawn_points = count_spawn_points(mapgroupproto_file)
    top_items = calculate_average_likelihood(item_data, usage_spawn_points)

    print(
        f"Top 20 Items Most Likely to Spawn with Usage '{usage_name}' (Average times found searching ten buildings):"
    )
    for item_name, likelihood in top_items:
        print(f" - {item_name}: {likelihood:.2f}")


if __name__ == "__main__":
    main()
