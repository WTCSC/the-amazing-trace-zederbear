# The Amazing Trace

[![Open in Codespaces](https://classroom.github.com/assets/launch-codespace-2972f46106e565e64193e422d61a12cf1da4916b45550586e14ef0a7c637dd04.svg)](https://classroom.github.com/open-in-codespaces?assignment_repo_id=18605999)

## Overview

The Amazing Trace is a Python project that performs traceroute operations to analyze network paths and display results visually. Using system commands and Python libraries, it:
- Executes traceroute commands to various destinations.
- Parses the traceroute output to extract hop details (IP, hostname, RTT).
- Aggregates and visualizes multiple traceroute attempts using Matplotlib.

## Features

- **Traceroute Execution:** Utilizes the `subprocess` module to run network traceroute commands.
- **Output Parsing:** Extracts structured information from traceroute output, handling timeouts and recorded round trip times.
- **Data Visualization:** Creates a plot of average round-trip times (RTT) per hop across multiple traces.
- **Customizable Parameters:** Allows configuration of the number of traces, interval between traces, and output directory for saved plots.

## Requirements

- Python 3.x
- [Matplotlib](https://matplotlib.org/)
- [Pandas](https://pandas.pydata.org/)
- [NumPy](https://numpy.org/)

You can install the required packages using pip:

```bash
pip install matplotlib pandas
```

Make sure you are using a virtual environment.

## Usage
Run the project with:
```bash
python amazing_trace.py
```
By default, the script runs traceroutes to a set of predefined destinations and saves the output plots to the output directory. You can modify the destinations or other parameters by editing the amazing_trace.py source code.

## Code Structure
- **amazing_trace.py**: Main source code file that contains functions for executing traceroute commands, parsing outputs, and visualizing the results.
- **README.md**: Project documentation and usage guide.

## Troubleshooting
- Ensure that the traceroute command is available on your system. On Windows, you might need to adjust the command (e.g., use `tracert` instead of `traceroute`).
- Confirm that all required Python packages are installed.