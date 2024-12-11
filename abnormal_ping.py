import time
import re

def abnormal_flow(net, abnormal_rtt_results):
    h1 = net.get('h1')
    s2 = net.get('s2')

    if 'ping_results' not in abnormal_rtt_results:
        abnormal_rtt_results['ping_results'] = []

    start_time = time.time()
    end_time = start_time + 30  # 測試持續 60 秒

    while time.time() < end_time:
        for _ in range(500):  # 每秒執行 500 次 Ping
            s2result = s2.cmd('ping -c 1 -W 1 %s' % h1.IP())
            rtt_pattern = re.compile(r'time=([\d\.]+) ms')
            match = rtt_pattern.search(s2result)
            if match:
                rtt = round(float(match.group(1)), 2)
                abnormal_rtt_results['ping_results'].append({
                    'source': s2.name,
                    'target': h1.name,
                    'rtt': rtt,
                    'timestamp': time.time()
                })
            time.sleep(0.002)  # 每次 Ping 間隔 2 毫秒

    print("Abnormal traffic finish.")
