# Manages the configuration file(s) for ChannelSimulator

def parse_config(filepath):
    """
    Parses a configuration file and returns a dictionary of key-value pairs.

    Args:
        filepath (str): The path to the configuration file.

    Returns:
        dict: A dictionary where keys are the configuration names (e.g., 'path', 'width')
              and values are their corresponding values (e.g., '/home/user1/...', 500).
              Comments (lines starting with '#') are ignored.
    """
    config = {}
    try:
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()  # Remove leading/trailing whitespace
                if line and not line.startswith('#'):  # Ignore empty lines and comments
                    if '=' in line:
                        key, value = line.split('=', 1)  # Split at the first '='
                        config[key.strip()] = value.strip()
    except FileNotFoundError:
        print(f"Error: Configuration file not found at {filepath}")
        return None
    return config

def parse_timestamps(filepath):
    """
    Parses a file containing timestamps and returns a list of timestamps.

    Args:
        filepath (str): The path to the file containing timestamps.

    Returns:
        list: A list of timestamps as strings.
    """
    timestamps = []
    try:
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()  # Remove leading/trailing whitespace
                if line and not line.startswith('#'):  # Ignore empty lines and comments
                    timestamps.append(line)
    except FileNotFoundError:
        print(f"Error: Timestamp file not found at {filepath}")
        return None
    return timestamps