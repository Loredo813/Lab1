import matplotlib.pyplot as plt

def plot_rtt_results(normal_rtt_results, title="RTT Over Time"):
    """
    繪製 RTT 結果的折線圖。

    :param normal_rtt_results: 包含 RTT 結果的字典，格式為
                               {'ping_results': [{'timestamp': 'HH:MM:SS', 'rtt': float}, ...]}
    :param title: 圖表標題
    """
    # 檢查數據是否存在
    if 'ping_results' not in normal_rtt_results or not normal_rtt_results['ping_results']:
        print("No RTT data available to plot.")
        return

    # 提取數據
    timestamps = [entry['timestamp'] for entry in normal_rtt_results['ping_results']]
    rtts = [entry['rtt'] for entry in normal_rtt_results['ping_results']]

    # 繪製圖表
    plt.figure(figsize=(12, 6))
    plt.plot(timestamps, rtts, marker='o', linestyle='-', alpha=0.7, label="RTT")

    # 設定圖表屬性
    plt.title(title, fontsize=16)
    plt.xlabel("Timestamp", fontsize=12)
    plt.ylabel("RTT (ms)", fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend(fontsize=10)
    plt.tight_layout()

    # 顯示圖表
    plt.show()
