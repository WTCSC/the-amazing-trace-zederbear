import unittest
import sys
import os
from amazing_trace import parse_traceroute

class TestParseTracerouteUnix(unittest.TestCase):
    """Test cases for parse_traceroute function specifically for Unix/Linux traceroute output."""

    def test_standard_unix_traceroute(self):
        """Test parsing standard Unix traceroute output."""
        unix_output = """
traceroute to google.com (142.250.185.78), 30 hops max, 60 byte packets
 1  _gateway (192.168.1.1)  1.235 ms  1.391 ms  1.506 ms
 2  192.168.100.1 (192.168.100.1)  4.782 ms  4.842 ms  4.897 ms
 3  router.isp (10.10.10.10)  10.123 ms  10.456 ms  10.789 ms
 4  core1.isp.net (20.20.20.20)  30.123 ms  30.456 ms  30.789 ms
 5  142.250.185.78 (142.250.185.78)  32.123 ms  32.456 ms  32.789 ms
        """

        result = parse_traceroute(unix_output)

        # Check number of hops
        self.assertEqual(len(result), 5)

        # Check first hop
        self.assertEqual(result[0]['hop'], 1)
        self.assertEqual(result[0]['ip'], '192.168.1.1')
        self.assertEqual(result[0]['hostname'], '_gateway')

        # Check RTT values are present without relying on order
        rtt_values = result[0]['rtt']
        self.assertEqual(len(rtt_values), 3)
        self.assertIn(1.235, rtt_values)
        self.assertIn(1.391, rtt_values)
        self.assertIn(1.506, rtt_values)

        # Check hop with IP and hostname
        self.assertEqual(result[2]['hop'], 3)
        self.assertEqual(result[2]['ip'], '10.10.10.10')
        self.assertEqual(result[2]['hostname'], 'router.isp')

        # Check last hop
        self.assertEqual(result[4]['hop'], 5)
        self.assertEqual(result[4]['ip'], '142.250.185.78')
        self.assertIsNone(result[4]['hostname'])  # No hostname for the final IP

    def test_unix_traceroute_with_timeouts(self):
        """Test parsing Unix traceroute output with timeouts."""
        timeout_output = """
traceroute to example.com (93.184.216.34), 30 hops max, 60 byte packets
 1  _gateway (192.168.1.1)  1.235 ms  1.391 ms  1.506 ms
 2  * * *
 3  10.0.0.1 (10.0.0.1)  15.123 ms * 15.789 ms
 4  * router2.isp (20.0.0.1)  20.456 ms *
 5  93.184.216.34 (93.184.216.34)  32.123 ms  32.456 ms  32.789 ms
        """

        result = parse_traceroute(timeout_output)

        # Check correct number of hops
        self.assertEqual(len(result), 5)

        # Check full timeout hop
        self.assertEqual(result[1]['hop'], 2)
        self.assertIsNone(result[1]['ip'])
        self.assertIsNone(result[1]['hostname'])
        self.assertEqual(result[1]['rtt'].count(None), 3)  # All three values should be None

        # Check mixed timeout hop
        self.assertEqual(result[2]['hop'], 3)
        self.assertEqual(result[2]['ip'], '10.0.0.1')
        self.assertIsNone(result[2]['hostname'])

        # Check RTT values contains expected values and correct number of timeouts
        rtt_values = result[2]['rtt']
        self.assertEqual(len(rtt_values), 3)
        self.assertEqual(rtt_values.count(None), 1)  # One timeout
        non_none_values = [v for v in rtt_values if v is not None]
        self.assertEqual(len(non_none_values), 2)  # Two valid RTT values
        self.assertIn(15.123, non_none_values)
        self.assertIn(15.789, non_none_values)

        # Check another mixed timeout pattern
        self.assertEqual(result[3]['hop'], 4)
        self.assertEqual(result[3]['ip'], '20.0.0.1')
        self.assertEqual(result[3]['hostname'], 'router2.isp')

        # Check RTT values contains expected values and correct number of timeouts
        rtt_values = result[3]['rtt']
        self.assertEqual(len(rtt_values), 3)
        self.assertEqual(rtt_values.count(None), 2)  # Two timeouts
        non_none_values = [v for v in rtt_values if v is not None]
        self.assertEqual(len(non_none_values), 1)  # One valid RTT value
        self.assertIn(20.456, non_none_values)

    def test_unix_traceroute_alternative_formats(self):
        """Test parsing Unix traceroute output with alternative formats."""
        alt_output = """
traceroute to github.com (140.82.121.3), 30 hops max
 1  router.home (192.168.1.1)  1.123 ms  1.456 ms  1.789 ms
 2  10.0.0.1  5.123 ms  5.456 ms  5.789 ms
 3  isp-router (172.16.0.1) <1 ms  0.5 ms  0.8 ms
 4  140.82.121.3  20.123 ms !X  20.456 ms !X  20.789 ms !X
        """

        result = parse_traceroute(alt_output)

        # Check correct number of hops
        self.assertEqual(len(result), 4)

        # Check hop with just IP (no parentheses)
        self.assertEqual(result[1]['hop'], 2)
        self.assertEqual(result[1]['ip'], '10.0.0.1')
        self.assertIsNone(result[1]['hostname'])

        # Check hop with small RTT values
        self.assertEqual(result[2]['hop'], 3)
        self.assertEqual(result[2]['hostname'], 'isp-router')
        self.assertEqual(result[2]['ip'], '172.16.0.1')

        # Check hop with extra markers (!X)
        self.assertEqual(result[3]['hop'], 4)
        self.assertEqual(result[3]['ip'], '140.82.121.3')
        self.assertIsNone(result[3]['hostname'])

        # Check for RTT values without relying on order
        rtt_values = result[3]['rtt']
        self.assertEqual(len(rtt_values), 3)
        expected_values = [20.123, 20.456, 20.789]
        for val in expected_values:
            self.assertTrue(any(abs(v - val) < 0.001 for v in rtt_values if v is not None),
                           f"Expected value {val} not found in RTT values {rtt_values}")

    def test_unix_traceroute_with_varying_hostname_formats(self):
        """Test parsing Unix traceroute output with varying hostname formats."""
        hostname_output = """
traceroute to mixed-hostnames.example.com (192.0.2.1), 30 hops max
 1  _gateway (192.168.1.1)  1.123 ms  1.456 ms  1.789 ms
 2  very.long.hostname.example.com (10.0.0.1)  5.123 ms  5.456 ms  5.789 ms
 3  node-with-dashes (172.16.0.1)  10.123 ms  10.456 ms  10.789 ms
 4  host_with_underscores (192.0.2.100)  15.123 ms  15.456 ms  15.789 ms
 5  192.0.2.1  20.123 ms  20.456 ms  20.789 ms
        """

        result = parse_traceroute(hostname_output)

        # Check correct number of hops
        self.assertEqual(len(result), 5)

        # Check long hostname
        self.assertEqual(result[1]['hop'], 2)
        self.assertEqual(result[1]['hostname'], 'very.long.hostname.example.com')
        self.assertEqual(result[1]['ip'], '10.0.0.1')

        # Check RTT values without relying on order
        rtt_values = result[1]['rtt']
        self.assertEqual(len(rtt_values), 3)
        expected_values = [5.123, 5.456, 5.789]
        for val in expected_values:
            self.assertTrue(any(abs(v - val) < 0.001 for v in rtt_values if v is not None),
                          f"Expected value {val} not found in RTT values {rtt_values}")

        # Check hostname with dashes
        self.assertEqual(result[2]['hop'], 3)
        self.assertEqual(result[2]['hostname'], 'node-with-dashes')
        self.assertEqual(result[2]['ip'], '172.16.0.1')

        # Check hostname with underscores
        self.assertEqual(result[3]['hop'], 4)
        self.assertEqual(result[3]['hostname'], 'host_with_underscores')
        self.assertEqual(result[3]['ip'], '192.0.2.100')

    def test_unix_traceroute_with_extra_info(self):
        """Test parsing Unix traceroute output with extra information."""
        extra_info_output = """
traceroute to google.com (142.250.185.78), 30 hops max, 60 byte packets
 1  _gateway (192.168.1.1)  1.235 ms  1.391 ms  1.506 ms
 2  192.168.100.1 (192.168.100.1)  4.782 ms  4.842 ms  4.897 ms
 3  router.isp (10.10.10.10)  10.123 ms !H  10.456 ms !N  10.789 ms !X
 4  asymmetric path  30.123 ms  30.456 ms  30.789 ms
 5  142.250.185.78 (142.250.185.78)  32.123 ms  32.456 ms  32.789 ms
        """

        result = parse_traceroute(extra_info_output)

        # The function should still extract the main data properly
        # even with extra markers like !H, !N, !X
        self.assertEqual(len(result), 5)
        self.assertEqual(result[2]['hop'], 3)
        self.assertEqual(result[2]['ip'], '10.10.10.10')
        self.assertEqual(result[2]['hostname'], 'router.isp')

    def test_unix_traceroute_empty_input(self):
        """Test parsing empty traceroute output."""
        empty_output = ""
        result = parse_traceroute(empty_output)
        self.assertEqual(result, [])

        whitespace_output = "\n\n   \n"
        result = parse_traceroute(whitespace_output)
        self.assertEqual(result, [])

    def test_unix_traceroute_with_non_standard_format(self):
        """Test parsing non-standard but valid Unix traceroute output."""
        non_standard_output = """
traceroute to example.com (93.184.216.34), 64 hops max
1  gateway (192.168.1.1)  1ms  1ms  2ms
2  isp.router (10.0.0.1)  5ms  6ms  5ms
3  * * *
4  example.com (93.184.216.34)  30ms  31ms  30ms
        """

        result = parse_traceroute(non_standard_output)

        # Function should be flexible enough to parse this format
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0]['hop'], 1)
        self.assertEqual(result[0]['hostname'], 'gateway')
        self.assertEqual(result[0]['ip'], '192.168.1.1')

    def test_unix_traceroute_with_multiple_ip_per_line(self):
        """Test parsing traceroute output with multiple IPs per line (unusual but possible)."""
        multiple_ip_output = """
traceroute to example.com (93.184.216.34), 30 hops max, 60 byte packets
 1  _gateway (192.168.1.1)  1.235 ms  1.391 ms  1.506 ms
 2  10.0.0.1 (10.0.0.1)  5.123 ms 10.0.0.2 (10.0.0.2)  5.456 ms 10.0.0.3 (10.0.0.3)  5.789 ms
 3  93.184.216.34 (93.184.216.34)  20.123 ms  20.456 ms  20.789 ms
        """

        result = parse_traceroute(multiple_ip_output)

        # Check how the function handles multiple IPs on one hop line
        # It should extract at least one valid IP from the line
        self.assertEqual(len(result), 3)
        self.assertEqual(result[1]['hop'], 2)
        self.assertIn(result[1]['ip'], ['10.0.0.1', '10.0.0.2', '10.0.0.3'])

if __name__ == '__main__':
    # Fix import - this is needed if the file names don't match Python module naming
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))

    # Import directly from the file if needed
    if 'amazing_trace' not in sys.modules:
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "amazing_trace",
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "amazing-trace.py")
        )
        amazing_trace = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(amazing_trace)
        # Replace the function with the directly imported one
        parse_traceroute = amazing_trace.parse_traceroute

    unittest.main()
