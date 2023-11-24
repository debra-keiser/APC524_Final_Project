import os
import re
from datetime import datetime, timedelta

from src.Read_Log_File import (
    extract_temperature,
    extract_time,
    round_to_tens_place,
    time_HMS_to_seconds,
)


def test_time_temp_extraction():
    """Check that the number of extracted experiment times and temperatures are equal."""
    with open(os.path.join("data/", "log.txt")) as open_file:
        individual_lines = open_file.readlines()

    recorded_times_from_experiment = []
    recorded_temperatures_from_experiment = []
    for line in individual_lines:
        if re.search(r"Synthetic_CSH_pdf.", line) is not None:
            recorded_times_from_experiment.append(extract_time(line))
            recorded_temperatures_from_experiment.append(
                float(extract_temperature(line))
            )

    assert len(recorded_times_from_experiment) == 117
    assert len(recorded_temperatures_from_experiment) == 117


def test_time_format():
    """Check that time in the log.txt file is in the expected format."""
    with open(os.path.join("data/", "log.txt")) as open_file:
        individual_lines = open_file.readlines()

    recorded_times_from_experiment = []
    for line in individual_lines:
        if re.search(r"Synthetic_CSH_pdf.", line) is not None:
            recorded_times_from_experiment.append(extract_time(line))

    for time in recorded_times_from_experiment:
        assert bool(datetime.strptime(time, "%H:%M:%S")) is True


def test_HMS_seconds():
    """Check that the time in H:M:S format is properly converted to seconds."""
    HMS = datetime.strptime("4:54:29", "%H:%M:%S")
    delta = timedelta(hours=HMS.hour, minutes=HMS.minute, seconds=HMS.second)

    assert time_HMS_to_seconds("4:54:29") == delta.total_seconds()


def test_tens_rounding():
    """Check that the temperature is properly rounded."""

    assert round_to_tens_place(134) == 130
    assert round_to_tens_place(78) == 80
