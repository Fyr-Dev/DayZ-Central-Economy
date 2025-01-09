# ...no existing code...
import re
import os


def split_categories(input_file, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    current_file = None
    current_category = None

    with open(input_file, "r", encoding="utf-8") as f:
        for line in f:
            match = re.search(
                r"<!-- #################### (.*?) #################### -->", line
            )
            if match:
                # Close previous file
                if current_file and not current_file.closed:
                    current_file.close()
                current_category = match.group(1).strip()
                out_path = os.path.join(output_dir, f"{current_category}.xml")
                current_file = open(out_path, "w", encoding="utf-8")
            if current_file:
                current_file.write(line)

    if current_file and not current_file.closed:
        current_file.close()


def main():
    input_path = r"c:\Users\lewis\Documents\GitHub\DayZ-Central-Economy\respawnOffline.charnarusplus\db\sorted_types (1).xml"
    output_directory = r"c:\Users\lewis\Documents\GitHub\DayZ-Central-Economy\respawnOffline.charnarusplus\db\categories"
    split_categories(input_path, output_directory)


if __name__ == "__main__":
    main()
