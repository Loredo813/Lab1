def plot_rtt_comparison(normal_rtt_results, abnormal_rtt_results, title="RTT Comparison: Normal vs Abnormal Traffic"):
    import matplotlib.pyplot as plt

    # 確認正常與異常流量的數據是否存在
    if not normal_rtt_results.get('ping_results') and not abnormal_rtt_results.get('ping_results'):
        print("No RTT data available to plot.")
        return

    # 處理正常流量數據
    normal_start_time = normal_rtt_results['ping_results'][0]['timestamp'] if normal_rtt_results.get('ping_results') else None
    normal_timestamps = [
        entry['timestamp'] - normal_start_time for entry in normal_rtt_results['ping_results']
    ] if normal_start_time else []
    normal_rtts = [entry['rtt'] for entry in normal_rtt_results['ping_results']] if normal_start_time else []

    # 處理異常流量數據
    abnormal_start_time = abnormal_rtt_results['ping_results'][0]['timestamp'] if abnormal_rtt_results.get('ping_results') else None
    abnormal_timestamps = [
        entry['timestamp'] - abnormal_start_time for entry in abnormal_rtt_results['ping_results']
    ] if abnormal_start_time else []
    abnormal_rtts = [entry['rtt'] for entry in abnormal_rtt_results['ping_results']] if abnormal_start_time else []

    # 開始繪圖
    plt.figure(figsize=(12, 6))

    # 繪製正常流量 RTT
        # 繪製正常流量 RTT
    if normal_timestamps and normal_rtts:
        plt.plot(
            normal_timestamps,
            normal_rtts,
            label="Normal Traffic",
            linestyle='-', color='blue', alpha=0.7  # 新增顏色
        )

    # 繪製異常流量 RTT
    if abnormal_timestamps and abnormal_rtts:
        plt.plot(
            abnormal_timestamps,
            abnormal_rtts,
            label="Abnormal Traffic",
            linestyle='--', color='red', alpha=0.7  # 新增顏色
        )


    # 設定圖表屬性
    plt.title(title, fontsize=14)
    plt.xlabel("Time (s)", fontsize=12)
    plt.ylabel("RTT (ms)", fontsize=12)
    plt.legend(fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()

    # 顯示圖表
    plt.show()
