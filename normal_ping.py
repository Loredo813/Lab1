import time
import re

def normal_flow(net, normal_rtt_results):
    h1 = net.get('h1')
    s1 = net.get('s1')

    if 'ping_results' not in normal_rtt_results:
        normal_rtt_results['ping_results'] = []

    end_time = time.time() + 60  # 結束時間為當前時間過 60 秒

    while time.time() < end_time:
        # 單次 Ping
        s1result = s1.cmd('sudo ping -c 100 -i 0.01 -W 1 %s' % h1.IP())
        rtt_pattern = re.compile(r'time=([\d\.]+) ms')
        match = rtt_pattern.search(s1result)
        if match:
            rtt = round(float(match.group(1)), 2)
            normal_rtt_results['ping_results'].append({
                'source': s1.name,
                'target': h1.name,
                'rtt': rtt,
                'timestamp': time.time()
            })
        else:
            continue

        time.sleep(1)  # 每秒測試一次

    print("Ping finish.")

