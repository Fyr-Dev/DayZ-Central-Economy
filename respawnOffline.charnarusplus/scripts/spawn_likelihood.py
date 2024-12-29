import xml.etree.ElementTree as ET
from collections import defaultdict


def parse_mapgrouppos(mapgrouppos_file):
    building_counts = defaultdict(int)
    tree = ET.parse(mapgrouppos_file)
    root = tree.getroot()

    # Looks for <group> elements
    for group_elem in root.findall("group"):
        bld_name = group_elem.get("name", "")
        count_value = int(group_elem.get("count", 1))
        building_counts[bld_name] += count_value

    return building_counts


def parse_mapgroupproto(mapgroupproto_file):
    building_info = {}
    tree = ET.parse(mapgroupproto_file)
    root = tree.getroot()

    for group in root.findall("group"):
        bld_name = group.get("name", "")
        # group_lootmax was already updated to match total points, so remove it below
        # group_lootmax = int(group.get("lootmax", 0))

        total_container_lootmax = 0
        total_points = 0
        for container in group.findall("container"):
            c_lootmax = int(container.get("lootmax", 0))
            total_container_lootmax += c_lootmax
            total_points += len(container.findall("point"))

        # Instead of adding group_lootmax, just use container total
        # total_lootmax = group_lootmax + total_container_lootmax
        total_lootmax = total_container_lootmax

        building_info[bld_name] = {
            "usage_names": [u.get("name") for u in group.findall("usage")],
            "total_lootmax": total_lootmax,
            "total_points": total_points,
        }

    return building_info


def parse_types(types_file):
    usage_nominal = defaultdict(int)
    usage_minimal = defaultdict(int)

    tree = ET.parse(types_file)
    root = tree.getroot()

    for t in root.findall("type"):
        nominal_elem = t.find("nominal")
        min_elem = t.find("min")
        nominal_val = int(nominal_elem.text) if nominal_elem is not None else 0
        minimal_val = int(min_elem.text) if min_elem is not None else 0

        for usage_elem in t.findall("usage"):
            usage_name = usage_elem.get("name")
            usage_nominal[usage_name] += nominal_val
            usage_minimal[usage_name] += minimal_val

    return usage_nominal, usage_minimal


def calculate_usage_totals(building_info, building_counts):
    usage_points = defaultdict(int)
    usage_lootmax = defaultdict(int)

    # Multiply building totals by how many times it appears
    for bld_name, info in building_info.items():
        times = building_counts.get(bld_name, 0)
        if times > 0:
            usage_pts = info["total_points"] * times
            usage_loot = info["total_lootmax"] * times
            for usage_name in info["usage_names"]:
                usage_points[usage_name] += usage_pts
                usage_lootmax[usage_name] += usage_loot

    return usage_points, usage_lootmax


def generate_spawn_report(types_file, mapgroupproto_file, mapgrouppos_file):
    building_counts = parse_mapgrouppos(mapgrouppos_file)
    building_info = parse_mapgroupproto(mapgroupproto_file)
    usage_nominal, usage_minimal = parse_types(types_file)
    usage_points, usage_lootmax = calculate_usage_totals(building_info, building_counts)

    # Gather all usage names
    all_usage_names = set(usage_points.keys()) | set(usage_nominal.keys())

    # For each usage, calculate chance = (nominal / lootmax)*100
    usage_stats = []
    for usage_name in all_usage_names:
        points = usage_points.get(usage_name, 0)
        loot = usage_lootmax.get(usage_name, 0)
        nom = usage_nominal.get(usage_name, 0)
        mini = usage_minimal.get(usage_name, 0)

        # Percent chance based on total item nominal vs total lootmax
        chance = (nom / loot * 100.0) if loot else 0.0

        usage_stats.append((usage_name, points, loot, chance, nom, mini))

    # Sort usage_stats by ascending chance
    usage_stats.sort(key=lambda r: r[3])

    print(
        "Spawn Report Summary (Lowest -> Highest Chance Based on Nominal vs Lootmax):"
    )
    for usage_name, pts, loot, chance, nom, mini in usage_stats:
        print(f"Usage: {usage_name}")
        print(f"  Total spawn points:   {pts}")
        print(f"  Total lootmax:        {loot}")
        print(f"  Sum of item nominal:  {nom}")
        print(f"  Sum of item minimal:  {mini}")
        print(f"  Chance per point:     {chance:.2f}%")
        print()

    # Overall totals across all usages
    total_points = sum(r[1] for r in usage_stats)
    total_lootmax = sum(r[2] for r in usage_stats)
    total_nominal = sum(r[4] for r in usage_stats)
    total_minimal = sum(r[5] for r in usage_stats)
    overall_chance = (total_nominal / total_lootmax * 100.0) if total_lootmax else 0.0

    print("Overall Game Totals:")
    print(f"  Total spawn points:   {total_points}")
    print(f"  Total lootmax:        {total_lootmax}")
    print(f"  Sum of item nominal:  {total_nominal}")
    print(f"  Sum of item minimal:  {total_minimal}")
    print(f"  Chance per point:     {overall_chance:.2f}%")


if __name__ == "__main__":
    generate_spawn_report(
        "C:/Users/lewis/Documents/GitHub/DayZ-Central-Economy/respawnOffline.charnarusplus/db/types.xml",
        "C:/Users/lewis/Documents/GitHub/DayZ-Central-Economy/respawnOffline.charnarusplus/mapgroupproto.xml",
        "C:/Users/lewis/Documents/GitHub/DayZ-Central-Economy/respawnOffline.charnarusplus/mapgrouppos.xml",
    )
