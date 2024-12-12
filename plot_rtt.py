def plot_rtt_results(normal_rtt_results, title="RTT Over Time"):
    import matplotlib.pyplot as plt

    # 檢查資料是否為空
    if not normal_rtt_results.get('ping_results'):
        print("No RTT data available to plot.")
        return

    # 計算相對時間
    start_time = normal_rtt_results['ping_results'][0]['timestamp']
    normal_timestamps = [
        entry['timestamp'] - start_time for entry in normal_rtt_results['ping_results']
    ]
    normal_rtts = [entry['rtt'] for entry in normal_rtt_results['ping_results']]

    # 開始繪圖
    plt.figure(figsize=(12, 6))

    # 繪製折線圖
    plt.plot(
        normal_timestamps,
        normal_rtts,
        label="Normal Traffic",
        linestyle='-',  # 折線樣式
        marker='o',     # 數據點標記
        alpha=0.7       # 半透明效果
    )

    # 設定圖表屬性
    plt.title(title, fontsize=14)
    plt.xlabel("Time (s)", fontsize=12)
    plt.ylabel("RTT (ms)", fontsize=12)
    plt.legend(fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.5)  # 虛線網格
    plt.tight_layout()

    # 顯示圖表
    plt.show()
