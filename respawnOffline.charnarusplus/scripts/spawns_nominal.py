import xml.etree.ElementTree as ET
from collections import defaultdict


def review_spawn_rates(types_file, mapgroupproto_file, mapgrouppos_file):
    # 1. Parse mapgrouppos.xml to count the number of instances of each building type.
    tree_pos = ET.parse(mapgrouppos_file)
    root_pos = tree_pos.getroot()

    building_counts = defaultdict(int)

    for group in root_pos.findall("group"):
        building_name = group.get("name")
        if building_name:
            building_counts[building_name] += 1

    # 2. Parse mapgroupproto.xml to count spawn points and lootmax by usage/category.
    tree_proto = ET.parse(mapgroupproto_file)
    root_proto = tree_proto.getroot()

    usage_spawn_points = defaultdict(int)
    usage_lootmax = defaultdict(int)

    for group in root_proto.findall("group"):
        group_name = group.get("name")
        usage_elems = group.findall("usage")
        for usage_elem in usage_elems:
            usage_attr = usage_elem.get("name")
            if usage_attr:
                # Count the number of spawn points within each container in the group
                for container in group.findall("container"):
                    spawn_points = len(container.findall("point"))
                    total_spawn_points = spawn_points * building_counts[group_name]
                    usage_spawn_points[usage_attr] += total_spawn_points

                    # Sum up the lootmax values within each container
                    lootmax = container.get("lootmax")
                    if lootmax:
                        try:
                            total_lootmax = int(lootmax) * building_counts[group_name]
                            usage_lootmax[usage_attr] += total_lootmax
                        except ValueError:
                            pass

    # 3. Parse types.xml to count nominal sums by usage.
    tree_types = ET.parse(types_file)
    root_types = tree_types.getroot()

    usage_nominal = defaultdict(int)

    for type_elem in root_types.findall("type"):
        nominal_elem = type_elem.find("nominal")
        if nominal_elem is not None:
            try:
                nominal_val = int(nominal_elem.text)
            except (ValueError, TypeError):
                nominal_val = 0
        else:
            nominal_val = 0

        usage_elems = type_elem.findall("usage")
        for ue in usage_elems:
            usage_name = ue.get("name")
            if usage_name:
                usage_nominal[usage_name] += nominal_val

    # 4. Collect and sort results by items per point.
    results = []
    for usage_name, sum_nominal in usage_nominal.items():
        points = usage_spawn_points.get(usage_name, 0)
        lootmax_total = usage_lootmax.get(usage_name, 0)
        if points == 0:
            ratio = float("inf")  # To handle division by zero
        else:
            ratio = round(sum_nominal / points, 2)
        results.append((usage_name, points, lootmax_total, sum_nominal, ratio))

    results.sort(key=lambda x: x[4])  # Sort by ratio (items per point)

    # 5. Print sorted results.
    print("Spawn Rate Review (sorted by items per point):")
    for usage_name, points, lootmax_total, sum_nominal, ratio in results:
        print(f"- Usage '{usage_name}':")
        print(f"   Total spawn points: {points}")
        print(f"   Total lootmax: {lootmax_total}")
        print(f"   Sum of item nominal: {sum_nominal}")
        if points == 0:
            print("   No spawn points found for this usage.")
        else:
            print(f"   Ratio (items per point): {ratio}")
        print()


# Example usage:
review_spawn_rates(
    "C:/Users/lewis/Documents/GitHub/DayZ-Central-Economy/respawnOffline.charnarusplus/db/types.xml",
    "C:/Users/lewis/Documents/GitHub/DayZ-Central-Economy/respawnOffline.charnarusplus/mapgroupproto.xml",
    "C:/Users/lewis/Documents/GitHub/DayZ-Central-Economy/respawnOffline.charnarusplus/mapgrouppos.xml",
)
