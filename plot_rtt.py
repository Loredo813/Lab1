import matplotlib.pyplot as plt

def plot_rtt_results(normal_rtt_results, abnormal_rtt_results, title="RTT Over Time: Normal, Abnormal"):
    plt.figure(figsize=(12, 6))

    # Normal flow RTT
    if 'ping_results' in normal_rtt_results:
        normal_timestamps = [entry['timestamp'] for entry in normal_rtt_results['ping_results']]
        normal_rtts = [entry['rtt'] for entry in normal_rtt_results['ping_results']]
        plt.plot(normal_timestamps, normal_rtts, label="Normal Traffic", linestyle='-', alpha=0.7)

    # Abnormal flow RTT
    if 'ping_results' in abnormal_rtt_results:
        abnormal_timestamps = [entry['timestamp'] for entry in abnormal_rtt_results['ping_results']]
        abnormal_rtts = [entry['rtt'] for entry in abnormal_rtt_results['ping_results']]
        plt.plot(abnormal_timestamps, abnormal_rtts, label="Abnormal Traffic", linestyle='--', alpha=0.7)

    # Plot configuration
    plt.title(title)
    plt.xlabel("Timestamp (s)")
    plt.ylabel("RTT (ms)")
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()
