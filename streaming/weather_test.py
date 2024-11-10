import pytest
from . import weather

sample_inputs = [
    {
        "type": "sample",
        "stationName": "Cherry Station",
        "timestamp": 1672531200000,
        "temperature": 37.1
    },
    {
        "type": "sample",
        "stationName": "Apple Station",
        "timestamp": 1672531400000,
        "temperature": 37.7
    },
    {
        "type": "sample",
        "stationName": "Banana Station",
        "timestamp": 1672531600000,
        "temperature": 36.7
    },
    {
        "type": "sample",
        "stationName": "Banana Station",
        "timestamp": 1672531800000,
        "temperature": 35.9
    },
]

# test if input is missing type, should raise exception
def test_unknown_message():
    events = [
        {"unknown": "unknown"}
    ]

    with pytest.raises(ValueError, match="missing 'type' in message"):
        list(weather.process_events(events))


# test if input is of unknown type, should raise exception
def test_unknown_message_type():
    events = [
        {"type": "unknown"}
    ]

    with pytest.raises(ValueError, match="Unknown event type: unknown"):
        list(weather.process_events(events))


# test if sample inputs are accepted correctly
def test_sample_input():
    expected_outputs = []

    assert expected_outputs == list(weather.process_events(sample_inputs))


# test if sample input are accepted correctly with output
def test_sample_snapshot():
    events = sample_inputs + [{
        "type": "control",
        "command": "snapshot"
    }]

    expected_outputs = [
        {
            "type": "snapshot",
            "asOf": 1672531800000,
            "stations": {
                "Cherry Station": {"high": 37.1, "low": 37.1},
                "Apple Station": {"high": 37.7, "low": 37.7},
                "Banana Station": {"high": 36.7, "low": 35.9}
            }
        }
    ]

    assert expected_outputs == list(weather.process_events(events))

# test if snapshot is correctly ignored with no samples
def test_snapshot_without_samples():
    events = [{
        "type": "control",
        "command": "snapshot"
    }]

    expected_outputs = []

    assert expected_outputs == list(weather.process_events(events))

# test sample reset is correctly handled
def test_sample_reset():
    events = sample_inputs + [{
        "type": "control",
        "command": "reset"
    }]

    expected_outputs = [
        {
            "type": "reset",
            "asOf": 1672531800000
        }
    ]
    assert expected_outputs == list(weather.process_events(events))

# test if reset is correctly ignored with no samples
def test_reset_without_samples():
    events = [{
        "type": "control",
        "command": "reset"
    }]

    expected_outputs = []

    assert expected_outputs == list(weather.process_events(events))

# test if unknown control command will raise error
def test_unknown_control_command():
    events = sample_inputs + [{
        "type": "control",
        "command": "unknown"
    }]
    with pytest.raises(ValueError, match="Unknown control command: unknown"):
        list(weather.process_events(events))

def test_sample_missing_station_timestamp():
    events = [{
        "type": "sample",
        "stationName": "Cherry Station",

        "temperature": 37.1
    }]

    with pytest.raises(ValueError, match="Sample timestamp is missing."):
        list(weather.process_events(events))

# test if sample missing station name would raise error
def test_sample_missing_station_name():
    events = [{
        "type": "sample",

        "timestamp": 1672531400000,
        "temperature": 37.1
    }]

    with pytest.raises(ValueError, match="Sample station name is missing."):
        list(weather.process_events(events))

# test if sample missing temperature would raise error
def test_sample_missing_station_temperature():
    events = [{
        "type": "sample",
        "stationName": "Cherry Station",
        "timestamp": 1672531400000,

    }]

    with pytest.raises(ValueError, match="Sample temperature is missing."):
        list(weather.process_events(events))
