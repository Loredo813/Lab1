import time
import re

def normal_flow(net, normal_rtt_results):
    h1 = net.get('h1')
    s1 = net.get('s1')

    # Regex pattern to extract RTT
    rtt_pattern = r"time=(\d+\.\d+) ms"

    start_time = time.time()  # Record the starting time of the ping loop

    try:
        while True:
            # Execute ping command
            result = s1.cmd(f'ping -c 1 {h1.IP()}')

            # Search for RTT in the output
            match = re.search(rtt_pattern, result)
            current_time = time.time()
            relative_time = current_time - start_time

            if match:
                rtt = float(match.group(1))  # Extract RTT in milliseconds
                normal_rtt_results.append((current_time, relative_time, rtt))  # Append timestamp, relative time, and RTT
                print(f"Ping successful, RTT: {rtt} ms, Timestamp: {current_time}, Relative Time: {relative_time:.2f} s")
            else:
                print(f"Ping failed or RTT not found. Timestamp: {current_time}, Relative Time: {relative_time:.2f} s")

            # Wait for 1 second before the next ping
            time.sleep(1)
    except KeyboardInterrupt:
        print("Ping loop interrupted by user.")
    except Exception as e:
        print(f"An error occurred: {e}")

