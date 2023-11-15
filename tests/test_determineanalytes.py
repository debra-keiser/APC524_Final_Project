from src.Determine_Analytes import (
    analyte_data,
    divide_by_100,
    list_item_differences,
    times_of_target_occurrence,
)
from src.Read_Log_File import extract_time_temp_data


def test_analyte_determination():
    """Check that the number of analyte times and temperatures are equal."""
    (
        recorded_times_from_experiment,
        recorded_temperatures_from_experiment,
        rounded_temperatures,
    ) = extract_time_temp_data("log.txt")
    analyte_times, analyte_temperatures = analyte_data(
        recorded_times_from_experiment,
        recorded_temperatures_from_experiment,
        rounded_temperatures,
    )
    assert len(analyte_times) == 107
    assert len(analyte_temperatures) == 107


def test_divide_100():
    """Check that the input is properly divided by 100."""
    assert divide_by_100(100) == 1


def test_target_occurrences():
    """Check that the expected index and complementary data is returned."""
    index, mock_times = times_of_target_occurrence(4, [1, 4, 3, 4, 5], [6, 7, 8, 9, 10])
    assert index == 4
    assert mock_times == [7, 9]


def test_item_differences():
    """Check that the items in a list are properly subtracted by its first item."""
    differences_list = list_item_differences([5, 32, 108])
    assert differences_list == [0, 27, 103]
