import re
import os
import logging
from time import perf_counter


def driver(file_name: str | os.PathLike) -> list:
    try:
        start = perf_counter()

        raw = extract_skus(file_name)
        formatted = format_skus(raw)
        write_skus(formatted, file_name)

        end = perf_counter()
    except (FileNotFoundError, PermissionError, IsADirectoryError, UnicodeDecodeError):
        logging.error("Double check your input file and try again")
        exit()

    logging.info("Format Completed in %.4f", end - start)

    return formatted


def extract_skus(file_name: str | os.PathLike) -> list[str]:
    raw_sku_list = []

    with open(file_name, "r") as file:
        for line in file:
            # "\d" means decimal digits and "+" means 1 or more times
            raw_skus = re.findall(r"\d+", line)
            for sku in raw_skus:
                raw_sku_list.append(sku)

    return raw_sku_list


def format_skus(raw_sku_list: list) -> list[str]:
    formatted_sku_list = []

    for raw_sku in raw_sku_list:
        # ^ means starts with 0 and replaces it with nothing (stripping the zeros)
        stripped_sku = re.sub('^0+', '', raw_sku)
        if stripped_sku == '':
            continue
        else:
            formatted_sku_list.append(stripped_sku)

    # dictionaries dedupe and keep order
    deduped_sku_dictionary = dict.fromkeys(formatted_sku_list, 0)

    deduped_sku_list = list(deduped_sku_dictionary.keys())

    return deduped_sku_list


def write_skus(deduped_sku_list: list, file_name: str | os.PathLike) -> None:
    with open(file_name, "w") as file:
        for index, sku in enumerate(deduped_sku_list):
            formatted_sku = (f"'{sku}'")
            if index < len(deduped_sku_list) - 1:
                file.write(f"{formatted_sku},\n")
            else:
                file.write(formatted_sku)
