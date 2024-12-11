import math

def calculate_average_rtt(normal_rtt_results):
    
    # 提取有效的 RTT 值
    rtt_values = [entry['rtt'] for entry in normal_rtt_results['ping_results'] if entry['rtt'] is not None]

    # 計算平均 RTT
    average_rtt = sum(rtt_values) / len(rtt_values)
    min_rtt = min(rtt_values)
    max_rtt = max(rtt_values)
    variance = sum((x - average_rtt) ** 2 for x in rtt_values) / len(rtt_values)
    std_deviation = math.sqrt(variance)

    # 返回結果字典
    return {
        'average': round(average_rtt, 2),
        'min': round(min_rtt, 2),
        'max': round(max_rtt, 2),
        'std_deviation': round(std_deviation, 2)
    }
