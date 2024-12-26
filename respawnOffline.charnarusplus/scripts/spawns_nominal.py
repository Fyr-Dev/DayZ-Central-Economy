import xml.etree.ElementTree as ET
from collections import defaultdict


def review_spawn_rates(types_file, mapgroupproto_file):
    # 1. Parse mapgroupproto.xml to count spawn points and lootmax by usage/category.
    tree_proto = ET.parse(mapgroupproto_file)
    root_proto = tree_proto.getroot()

    # Dictionary: usage_name -> count of groups and total lootmax
    usage_spawn_points = defaultdict(int)
    usage_lootmax = defaultdict(int)

    # Example assumption: mapgroupproto has <group name="NAME" usage="USAGE" ...>
    for group in root_proto.findall("group"):
        usage_elems = group.findall("usage")
        for usage_elem in usage_elems:
            usage_attr = usage_elem.get("name")
            if usage_attr:
                # Count the number of spawn points within each container in the group
                for container in group.findall("container"):
                    spawn_points = len(container.findall("point"))
                    usage_spawn_points[usage_attr] += spawn_points

                    # Sum up the lootmax values within each container
                    lootmax = container.get("lootmax")
                    if lootmax:
                        try:
                            usage_lootmax[usage_attr] += int(lootmax)
                        except ValueError:
                            pass

    # 2. Parse types.xml to count nominal sums by usage.
    tree_types = ET.parse(types_file)
    root_types = tree_types.getroot()

    # usage_name -> sum of nominal
    usage_nominal = defaultdict(int)

    for type_elem in root_types.findall("type"):
        # Gather nominal.
        nominal_elem = type_elem.find("nominal")
        if nominal_elem is not None:
            try:
                nominal_val = int(nominal_elem.text)
            except (ValueError, TypeError):
                nominal_val = 0
        else:
            nominal_val = 0

        # Gather usage tags.
        usage_elems = type_elem.findall("usage")
        # e.g. <usage name="Military" />
        # Some items might have more than one usage, add the item’s nominal to each usage.
        for ue in usage_elems:
            usage_name = ue.get("name")
            if usage_name:
                usage_nominal[usage_name] += nominal_val

    # 3. Print comparison for each usage found in types.
    print("Spawn Rate Review:")
    for usage_name, sum_nominal in usage_nominal.items():
        points = usage_spawn_points.get(usage_name, 0)
        lootmax_total = usage_lootmax.get(usage_name, 0)
        print(f"- Usage '{usage_name}':")
        print(f"   Total spawn points: {points}")
        print(f"   Total lootmax: {lootmax_total}")
        print(f"   Sum of item nominal: {sum_nominal}")
        if points == 0:
            print("   No spawn points found for this usage.")
        else:
            ratio = round(sum_nominal / points, 2)
            print(f"   Ratio (items per point): {ratio}")
        print()


# Example usage:
review_spawn_rates(
    "C:/Users/lewis/Documents/GitHub/DayZ-Central-Economy/respawnOffline.charnarusplus/db/types.xml",
    "C:/Users/lewis/Documents/GitHub/DayZ-Central-Economy/respawnOffline.charnarusplus/mapgroupproto.xml",
)
