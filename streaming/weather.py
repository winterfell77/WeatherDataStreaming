from typing import Any, Iterable, Generator

def process_snapshot_command(most_recent_timestamp, station_temperatures):
    snapshot_response = {
        "type": "snapshot",
        "asOf": most_recent_timestamp,
        "stations": station_temperatures,
    }
    yield snapshot_response

def process_reset_command(most_recent_timestamp):
    reset_response = {
        "type": "reset",
        "asOf": most_recent_timestamp,
    }
    yield reset_response

def process_weather_sample(weather_sample, station_temperatures, most_recent_timestamp):
    sample_station = weather_sample.get("stationName")
    sample_timestamp = weather_sample.get("timestamp")
    sample_temperature = weather_sample.get("temperature")

    if sample_station is None:
        raise ValueError("Sample station name is missing.")
    if sample_timestamp is None:
        raise ValueError("Sample timestamp is missing.")
    if sample_temperature is None:
        raise ValueError("Sample temperature is missing.")

    if most_recent_timestamp is None:
        most_recent_timestamp = sample_timestamp
    else:
        most_recent_timestamp = max(most_recent_timestamp, sample_timestamp)

    if sample_station not in station_temperatures:
        station_temperatures[sample_station] = {
            "high": sample_temperature,
            "low": sample_temperature,
        }
    else:
        station_temperatures[sample_station]["high"] = (
            max(station_temperatures[sample_station]["high"], sample_temperature))
        station_temperatures[sample_station]["low"] = (
            min(station_temperatures[sample_station]["low"], sample_temperature))
    return station_temperatures, most_recent_timestamp

def process_events(events: Iterable[dict[str, Any]]) -> Generator[dict[str, Any], None, None]:
    station_temperatures: dict[str, dict[str, float]] = {}
    most_recent_timestamp: int | None = None

    for event in events:
        if "type" not in event:
            raise ValueError("missing 'type' in message")
        event_type = event["type"]

        if event_type == "sample":
            station_temperatures, most_recent_timestamp = (
                process_weather_sample(event, station_temperatures, most_recent_timestamp))
        elif event_type == "control":
            if most_recent_timestamp is None:
                continue
            control_command = event["command"]

            if control_command == "snapshot":
                yield from process_snapshot_command(most_recent_timestamp, station_temperatures)
            elif control_command == "reset":
                yield from process_reset_command(most_recent_timestamp)
                most_recent_timestamp = None
                station_temperatures.clear()
            else:
                raise ValueError(f"Unknown control command: {control_command}")
        else:
            raise ValueError(f"Unknown event type: {event_type}")
