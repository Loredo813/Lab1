def plot_rtt_results(normal_rtt_results, title="RTT Over Time"):
    import matplotlib.pyplot as plt

    plt.figure(figsize=(12, 6))

    # 計算相對時間
    start_time = min(
        normal_rtt_results['ping_results'][0]['timestamp'],
    )
    normal_timestamps = [entry['timestamp'] - start_time for entry in normal_rtt_results['ping_results']]
   
    # 正常流量
    normal_rtts = [entry['rtt'] for entry in normal_rtt_results['ping_results']]
    plt.plot(normal_timestamps, normal_rtts, label="Normal Traffic", linestyle='-', alpha=0.7)


    plt.title(title)
    plt.xlabel("Time (s)")
    plt.ylabel("RTT (ms)")
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()
