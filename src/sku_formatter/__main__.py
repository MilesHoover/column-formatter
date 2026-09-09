import argparse
import logging

from . import sku_formatter


def get_file_name():
    parser = argparse.ArgumentParser(
        prog="column-formatter", description="A program to format SKUs"
    )
    parser.add_argument(
        "file_name", help="The name of the text file containing skus to format"
    )
    args = parser.parse_args()
    file_name = args.file_name

    return file_name


def main():
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    file_name = get_file_name()
    sku_formatter.driver(file_name)


if __name__ == "__main__":
    main()
