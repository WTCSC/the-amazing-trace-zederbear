# Requirements

In this assignment, you'll be using Python to analyze traceroute data, giving you hands-on experience with both networking concepts and basic data analysis techniques.

## Overview

For this coding exercise, you'll be creating two essential functions:

1. `execute_traceroute(destination)`: A function that runs the traceroute command for a given destination and returns the raw output
2. `parse_traceroute(traceroute_output)`: A function that parses the raw traceroute output into a structured format

The starter code provided will use your functions to create visualizations that help analyze routing patterns.  Your task is to complete the following two functions (as found in the `amazing-trace.py` file within the GitHub assignment):

```python
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
    pass
```

```python
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

    Example Return:
        [
					    {
					        'hop': 1,
					        'ip': '172.21.160.1',
					        'hostname': '[HELDMANBACK.mshome.net](http://HELDMANBACK.mshome.net)',
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
    """
    # Your code here
    # Hint: Use regular expressions to extract the relevant information
    # Handle timeouts (asterisks) appropriately
    pass
```

When properly completed and executed, the `amazing-race.py` file *and* unit tests (via `pytest`) should all successfully complete, resulting in a visualization of each traceroute run in the `output/` directory of the project.

## Tips for Success

- **Linux**: Utilize the included `Vagrantfile` to create a virtualized Linux environment for testing. This approach ensures your code works consistently across different systems and provides a controlled environment for network operations.
- **ICMP Packets**: Remember to use the `-I` option with the traceroute command when running on Linux to force the use of ICMP packets, which are more likely to accurately represent real-world packet routing. This is especially important when tracing through networks that may filter or prioritize different protocols.
- **Handling subprocesses:** Use Python's `subprocess.run()` or `subprocess.check_output()` to execute the traceroute command.
- **Regular expressions:** Use the `re` module to parse the traceroute output effectively.
- **Error handling:** Make sure your functions handle cases like timeouts and errors gracefully.
- **Testing:** Test your functions with different destinations to ensure they work correctly by running the script within a Linux environment (`python3 amazing-trace.py`) *and* running the included unit tests, which will test your `parse_traceroute()` function specifically (`pytest test_amazing_trace.py`).

## Evaluation

### Code Completeness - 50 pts possible

This score will be determined by the result of running a series of automated tests on your code. The tests check whether your code implements the tasks we ask you to implement in the assignment and, thus, are a good measure of how complete your code is.

#### 50 pts

Code met all defined acceptance criteria and all automated tests pass.

#### 30 pts

Either some defined acceptance criteria was not met, or some automated tests did not pass.

#### 0 pts

None of the defined acceptance criteria was met and none of the automated tests passed.

### Code Readability - 25 pts possible

This score will be determined by qualities, many of which are intangible, that don’t have to do with (and exist to some extent independently of) the correct operation of your code.

#### 25 pts
The code is well-structured and easy to read. Variables were appropriately named, and whitespace was used to clearly separate logical concepts.

#### 15 pts

Improvement could be made to the structure and readability of the code. Variables were unclear, whitespace wasn't effectively utilized, or other issues made the code difficult to parse.

#### 0 pts

Code followed non-standard formatting or uses inappropriate variable names.

#### Code Correctness - 25 pts possible

This score encompasses issues with your code that, while not explicitly captured by the tests, could lead to incorrect behavior (or simply neglect to implement something we told you to implement). This section of the rubric will never re-penalize you for a failure that is already captured by the "Completeness" score.

#### 25 pts

There is no inadvertent behavior, problematic scale issues, or other unexpected/unnecessary operations in the code.

#### 15 pts

There is no inadvertent behavior or unexpected/unnecessary operations in the code, but the implementation will not hold up under large scale.

#### 0 pts

The code performs unnecessary operations or has problematic downstream consequences.

### Documentation Clarity - 20 pts possible

This score evaluates how well the documentation communicates the purpose and functionality of the code to the reader.

#### 20 pts

Clear, concise, and well-structured documentation. Code comments explain why key sections of code exist, not just what they do. Supplemental documentation (README, user manual) provides detailed explanations of setup, usage, and examples. Consistent formatting and language throughout.

#### 10 pts

Documentation is present but lacks clarity in some areas. Code comments are mostly what the code does, with minimal explanation of why. Supplemental documentation explains the basics but may be incomplete or unclear in certain sections. Inconsistent formatting or language in some parts.

#### 0 pts

Documentation is unclear or missing. Minimal or no code comments. Supplemental documentation, if present, is confusing or irrelevant. Poor or inconsistent structure and formatting.

### Documentation Accuracy - 20 pts possible

This score measures the correctness of the information provided in the documentation, ensuring it aligns with the actual code functionality.

#### 20 pts

Documentation accurately reflects the code’s functionality. Code comments match the behavior of the corresponding code. Supplemental documentation correctly explains setup, functionality, and output with no errors.

#### 10 pts

Documentation is mostly accurate, but with minor errors or omissions. Some code comments may not fully match the current implementation. Supplemental documentation may have minor inaccuracies or missing details.

#### 0 pts

Documentation is mostly or entirely inaccurate. Code comments misrepresent what the code does. Supplemental documentation contains significant errors or missing critical information.

### Documentation Completeness

This score assesses whether the documentation covers all necessary aspects of the code, including setup, usage, and edge cases.

#### 10 pts

Documentation is complete. All key parts of the code are commented. Supplemental documentation includes setup instructions, usage examples, and explanations of any edge cases or assumptions.

#### 5 pts

Documentation is mostly complete but may miss some minor details. Key parts of the code are commented, but less critical sections may be omitted. Supplemental documentation covers setup and basic usage but omits edge cases or assumptions.

#### 0 pts

Documentation is incomplete. Critical sections of code are uncommented. Supplemental documentation is missing or lacks key sections (e.g., setup, usage).
