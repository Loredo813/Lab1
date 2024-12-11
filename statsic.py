import numpy as np

def calculate_rtt_statistics(rtt_results):
    """
    計算 RTT 的平均值、最大值、最小值和標準差。

    :param rtt_results: 包含 RTT 數據的字典，例如：
                        {
                            'ping_results': [
                                {'rtt': 12.5, 'timestamp': 1},
                                {'rtt': 14.2, 'timestamp': 2},
                                ...
                            ]
                        }
    :return: 包含統計結果的字典，例如：
             {
                 'average': 13.35,
                 'max': 14.2,
                 'min': 12.5,
                 'std_deviation': 0.85
             }
    """
    if not rtt_results.get('ping_results'):
        return None  # 如果沒有 RTT 數據，返回 None

    rtt_values = [entry['rtt'] for entry in rtt_results['ping_results']]
    if not rtt_values:
        return None  # 如果 RTT 數據為空，返回 None

    # 計算統計數據
    avg_rtt = np.mean(rtt_values)
    max_rtt = np.max(rtt_values)
    min_rtt = np.min(rtt_values)
    std_rtt = np.std(rtt_values)

    return {
        'average': round(avg_rtt, 2),
        'max': round(max_rtt, 2),
        'min': round(min_rtt, 2),
        'std_deviation': round(std_rtt, 2)
    }
