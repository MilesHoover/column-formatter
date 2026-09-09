import pytest

from sku_formatter import sku_formatter


def test_format_skus_strips_leading_zeros():
    assert sku_formatter.format_skus(["00123456", "001234567"]) == ["123456", "1234567"]


def test_format_skus_dedupes():
    assert sku_formatter.format_skus(
        ["987654321", "123456789", "987654321", "1234567891"]
    ) == ["987654321", "123456789", "1234567891"]


def test_format_skus_avoids_all_zero_input():
    assert sku_formatter.format_skus(["000000", "00000000000"]) == []


def test_format_skus_avoids_empty_input():
    assert sku_formatter.format_skus([]) == []


@pytest.fixture(scope="session")
def input_file(tmp_path_factory):
    directory = tmp_path_factory.mktemp("directory")
    file = directory / "input.txt"
    file.write_text(
        "21341234 040124109491 000102341234 asdfsf241234   !!! 2134234 21341234"
    )
    return file


def test_extract_skus(input_file):
    assert sku_formatter.extract_skus(input_file) == [
        "21341234",
        "040124109491",
        "000102341234",
        "241234",
        "2134234",
        "21341234",
    ]


def test_extract_skus_no_digits(tmp_path):
    no_digits_input = tmp_path / "no_digits_input.txt"
    no_digits_input.write_text("")
    assert sku_formatter.extract_skus(no_digits_input) == []


@pytest.fixture(scope="session")
def write_skus_input_file(tmp_path_factory):
    directory = tmp_path_factory.mktemp("directory")
    write_skus_input = directory / "write_skus_input.txt"
    return write_skus_input


def test_write_skus(write_skus_input_file):
    sku_formatter.write_skus(
        ["21341234", "40124109491", "102341234", "241234", "2134234"],
        write_skus_input_file,
    )
    assert (
        write_skus_input_file.read_text()
        == "'21341234',\n'40124109491',\n'102341234',\n'241234',\n'2134234'"
    )


def test_write_skus_empty_list(tmp_path):
    write_skus_input = tmp_path / "write_skus_input.txt"
    sku_formatter.write_skus([], write_skus_input)
    assert write_skus_input.read_text() == ""


def test_driver(tmp_path):
    driver_input = tmp_path / "driver_input.txt"
    driver_input.write_text("""
        94812370, 0041234736 --comment #123#
        
        94812370 --this should be deduped!!
        0091912y923444_
        
        
        fasdfasdf a3123412341234 ffff 312341234fjf
        """)
    sku_formatter.driver(driver_input)
    assert (
        driver_input.read_text()
        == "'94812370',\n'41234736',\n'123',\n'91912',\n'923444',\n'3123412341234',\n'312341234'"
    )


def test_driver_exception(tmp_path):
    driver_exception_input = tmp_path / "driver_exception_input.txt"
    with pytest.raises(SystemExit):
        sku_formatter.driver(driver_exception_input)
