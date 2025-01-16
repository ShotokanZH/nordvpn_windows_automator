# NordVPN Automation Script

This script provides a Python-based interface to manage NordVPN connections, allowing for automated connections based on servers or countries, as well as manual disconnections. It integrates the NordVPN command-line tool with additional functionality, such as checking your current IP and updating it post-connection.

## Features

- **Automatic Connection**: Connects to the best available server automatically.
- **Server-based Connection**: Connects to a specified NordVPN server by name.
- **Country-based Connection**: Connects to the best server in a specified country.
- **Disconnection**: Disconnects from the current NordVPN session.
- **IP Monitoring**: Tracks your public IP address before and after connection/disconnection.
- **Real-Time Feedback**: Indicates connection progress in real-time.

## Prerequisites

1. **Python 3.6+**
2. **NordVPN Command-Line Tool (`nordvpn.exe`)**: Ensure it's installed and accessible in your system's PATH.
3. **Required Python Libraries**:
   - `requests`
   - `argparse`
4. **Internet Access**: For retrieving server and IP data.

Install dependencies using:
```bash
pip install requests
```

## Usage

Run the script with the appropriate arguments:

### Options

- `--auto`: Connects to the best available server automatically.
- `--server <server_name>`: Connects to a specific NordVPN server by its name.
- `--country <country_name>`: Connects to the best server in the specified country.
- `--disconnect`: Disconnects from the current VPN session.

### Examples

#### Automatic Connection
```bash
python3 nordvpn_script.py --auto
```

#### Connect to a Specific Server
```bash
python3 nordvpn_script.py --server us1234.nordvpn.com
```

#### Connect to a Specific Country
```bash
python3 nordvpn_script.py --country Germany
```

#### Disconnect
```bash
python3 nordvpn_script.py --disconnect
```

## How It Works

1. **Server and Country Retrieval**: The script fetches the list of available servers and countries from NordVPN's public API.
2. **Connection**: Executes NordVPN commands to establish a connection based on user input (auto, server, or country).
3. **IP Change Monitoring**: Ensures the public IP changes after a successful connection or disconnection.
4. **Error Handling**: Provides feedback if the specified server or country is invalid.

## Notes

- Ensure you are logged into NordVPN using the command-line tool before running the script.
- For country names, the script capitalizes the first letter automatically (e.g., "germany" → "Germany").
- If the server or country specified is invalid, the script will raise an error and display available options.
