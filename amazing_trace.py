import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.ticker import MaxNLocator
import time
import os
import subprocess
import re

def execute_traceroute(destination):
    """
    Executes a traceroute to the specified destination and returns the output.

    Args:
        destination (str): The hostname or IP address to trace

    Returns:
        str: The raw output from the traceroute command
    """
    # Your code here
    # Hint: Use the subprocess module to run the traceroute command
    # Make sure to handle potential errors

    # Remove this line once you implement the function,
    # and don't forget to *return* the output

    output = subprocess.run(["traceroute", destination], capture_output=True)
    print(output.stdout.decode())
    return output.stdout.decode()

def parse_traceroute(traceroute_output):
    """
    Parses the raw traceroute output into a structured format.

    Args:
        traceroute_output (str): Raw output from the traceroute command

    Returns:
        list: A list of dictionaries, each containing information about a hop:
            - 'hop': The hop number (int)
            - 'ip': The IP address of the router (str or None if timeout)
            - 'hostname': The hostname of the router (str or None if same as ip)
            - 'rtt': List of round-trip times in ms (list of floats, None for timeouts)

    Example:
    ```
        [
            {
                'hop': 1,
                'ip': '172.21.160.1',
                'hostname': 'HELDMANBACK.mshome.net',
                'rtt': [0.334, 0.311, 0.302]
            },
            {
                'hop': 2,
                'ip': '10.103.29.254',
                'hostname': None,
                'rtt': [3.638, 3.630, 3.624]
            },
            {
                'hop': 3,
                'ip': None,  # For timeout/asterisk
                'hostname': None,
                'rtt': [None, None, None]
            }
        ]
    ```
    """
    # Your code here
    # Hint: Use regular expressions to extract the relevant information
    # Handle timeouts (asterisks) appropriately

    # Remove this line once you implement the function,
    # and don't forget to *return* the output
    hops = []

    for line in traceroute_output.splitlines():
        line = line.strip()

        if not line or not re.match(r'^\d+\s', line):
            continue

        m = re.match(r'^(\d+)\s+(.*)', line)
        if not m:
            continue
        hop_num = int(m.group(1))
        rest = m.group(2)

        rtts = []
        for match in re.finditer(r'(?:<)?(\d+(?:\.\d+)?)\s*ms|(\*)', rest):
            if match.group(1):
                try:
                    rtts.append(float(match.group(1)))
                except ValueError:
                    rtts.append(None)
            else:
                rtts.append(None)
        
        while len(rtts) < 3:
            rtts.append(None)
        rtts = rtts[:3]

        host_ip_match = re.search(r'(\S+)\s+\((\d{1,3}(?:\.\d{1,3}){3})\)', rest)
        hostname = None
        ip = None
        if host_ip_match:
            possible_host = host_ip_match.group(1)
            possible_ip = host_ip_match.group(2)
            
            if re.match(r'^\d{1,3}(?:\.\d{1,3}){3}$', possible_host) and possible_host == possible_ip:
                hostname = None
            else:
                hostname = possible_host
            ip = possible_ip
        else:
            tokens = rest.split()
            if tokens:
                first = tokens[0]
                if re.match(r'^\d{1,3}(?:\.\d{1,3}){3}$', first):
                    ip = first

        hops.append({
            'hop': hop_num,
            'ip': ip,
            'hostname': hostname,
            'rtt': rtts
        })

    return hops

# ============================================================================ #
#                    DO NOT MODIFY THE CODE BELOW THIS LINE                    #
# ============================================================================ #
def visualize_traceroute(destination, num_traces=3, interval=5, output_dir='output'):
    """
    Runs multiple traceroutes to a destination and visualizes the results.

    Args:
        destination (str): The hostname or IP address to trace
        num_traces (int): Number of traces to run
        interval (int): Interval between traces in seconds
        output_dir (str): Directory to save the output plot

    Returns:
        tuple: (DataFrame with trace data, path to the saved plot)
    """
    all_hops = []

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    print(f"Running {num_traces} traceroutes to {destination}...")

    for i in range(num_traces):
        if i > 0:
            print(f"Waiting {interval} seconds before next trace...")
            time.sleep(interval)

        print(f"Trace {i+1}/{num_traces}...")
        output = execute_traceroute(destination)
        hops = parse_traceroute(output)

        # Add timestamp and trace number
        timestamp = time.strftime("%H:%M:%S")
        for hop in hops:
            hop['trace_num'] = i + 1
            hop['timestamp'] = timestamp
            all_hops.append(hop)

    # Convert to DataFrame for easier analysis
    df = pd.DataFrame(all_hops)

    # Calculate average RTT for each hop (excluding timeouts)
    df['avg_rtt'] = df['rtt'].apply(lambda x: np.mean([r for r in x if r is not None]) if any(r is not None for r in x) else None)

    # Plot the results
    plt.figure(figsize=(12, 6))

    # Create a subplot for RTT by hop
    ax1 = plt.subplot(1, 1, 1)

    # Group by trace number and hop number
    for trace_num in range(1, num_traces + 1):
        trace_data = df[df['trace_num'] == trace_num]

        # Plot each trace with a different color
        ax1.plot(trace_data['hop'], trace_data['avg_rtt'], 'o-',
                label=f'Trace {trace_num} ({trace_data.iloc[0]["timestamp"]})')

    # Add labels and legend
    ax1.set_xlabel('Hop Number')
    ax1.set_ylabel('Average Round Trip Time (ms)')
    ax1.set_title(f'Traceroute Analysis for {destination}')
    ax1.grid(True, linestyle='--', alpha=0.7)
    ax1.legend()

    # Make sure hop numbers are integers
    ax1.xaxis.set_major_locator(MaxNLocator(integer=True))

    plt.tight_layout()

    # Save the plot to a file instead of displaying it
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    safe_dest = destination.replace('.', '-')
    output_file = os.path.join(output_dir, f"trace_{safe_dest}_{timestamp}.png")
    plt.savefig(output_file)
    plt.close()

    print(f"Plot saved to: {output_file}")

    # Return the dataframe and the path to the saved plot
    return df, output_file

# Test the functions
if __name__ == "__main__":
    # Test destinations
    destinations = [
        "google.com",
        "amazon.com",
        "bbc.co.uk"  # International site
    ]

    for dest in destinations:
        df, plot_path = visualize_traceroute(dest, num_traces=3, interval=5)
        print(f"\nAverage RTT by hop for {dest}:")
        avg_by_hop = df.groupby('hop')['avg_rtt'].mean()
        print(avg_by_hop)
        print("\n" + "-"*50 + "\n")
