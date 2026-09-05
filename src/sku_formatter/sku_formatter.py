import re

def driver(file_name):
    try:
        raw = extract_skus(file_name)
        formatted = format_skus(raw)
        write_skus(formatted, file_name)
    except (FileNotFoundError, PermissionError, IsADirectoryError, UnicodeDecodeError):
        print("Double check your file and try again")
        exit()

    return formatted

def extract_skus(file_name):
    raw_sku_list = []

    with open(file_name, "r") as file:
        for line in file:
            raw_skus = re.findall(r"\d+", line) # "\d" means decimal digits and "+" means 1 or more times
            for sku in raw_skus:
                raw_sku_list.append(sku)

    return raw_sku_list

def format_skus(raw_sku_list):
    formatted_sku_list = []

    for raw_sku in raw_sku_list:
        stripped_sku = re.sub('^0+', '', raw_sku) # ^ means starts with 0 and replaces it with nothing (stripping the zeros)
        if stripped_sku == '':
            continue
        else:
            formatted_sku_list.append(stripped_sku)

    deduped_sku_dictionary = dict.fromkeys(formatted_sku_list, 0) # dictionaries dedupe and keep order

    deduped_sku_list = list(deduped_sku_dictionary.keys())

    return deduped_sku_list

def write_skus(deduped_sku_list, file_name):
    with open(file_name, "w") as file:
        for index, sku in enumerate(deduped_sku_list):
            formatted_sku = (f"'{sku}'")
            if index < len(deduped_sku_list) - 1:
                file.write(f"{formatted_sku},\n")
            else:
                file.write(formatted_sku)
    print("Format complete")