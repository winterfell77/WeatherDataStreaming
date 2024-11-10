# Weather Station Data Aggregator

## Purpose
Aggregates real-time weather data from multiple Chicago city beach stations, producing snapshots of the aggregated weather state on request.

## Input
The program receives a stream of JSON-formatted messages through STDIN. These messages can be of two types:
- **Weather Samples**: Real-time data from weather stations (e.g., temperature readings).
- **Control Commands**: Instructions to either generate a snapshot or reset the stored data.

## Functionality
- **Weather Sample Processing**:
    - Stores temperature data for each station.
    - Tracks high and low temperatures for each station.
    - Updates the most recent timestamp to reflect the latest data received.

- **Control Command Processing**:
    - **Snapshot Command**:
        - Outputs a JSON snapshot containing the high and low temperatures for each station as of the most recent timestamp.
    - **Reset Command**:
        - Clears all stored temperature data and resets the most recent timestamp.

## Output
The program outputs JSON-formatted responses to STDOUT based on the received control commands:
- **Snapshot**: Provides the current aggregated weather data across stations.
- **Reset**: Confirms that all stored data has been cleared.

## Error Handling
- Ensures that all required fields are present in incoming messages.
- Raises errors for unknown event types or commands to maintain data integrity.
