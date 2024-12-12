import time
import re

def normal_flow(net, normal_rtt_results):
    h1 = net.get('h1')
    s1 = net.get('s1')

    # 初始化結果字典
    normal_rtt_results.setdefault('ping_results', [])

    end_time = time.time() + 60  # 結束時間為當前時間過 60 秒

    while time.time() < end_time:
        # 單次 Ping
        s1result = s1.cmd(f'ping -c 1 -s 64 -W 1 {h1.IP()}')
        
        # 匹配 RTT
        rtt_pattern = re.compile(r'time=([\d\.]+) ms')
        match = rtt_pattern.search(s1result)

        # 紀錄結果
        current_time = time.strftime('%H:%M:%S', time.localtime())
        if match:
            rtt = round(float(match.group(1)), 2)
            normal_rtt_results['ping_results'].append({
                'source': s1.name,
                'target': h1.name,
                'rtt': rtt,
                'timestamp': current_time
            })
            print(f"[{current_time}] Success: RTT={rtt} ms (Source: {s1.name}, Target: {h1.name})")
        else:
            print(f"[{current_time}] Ping failed: No RTT recorded (Source: {s1.name}, Target: {h1.name})")
        
        # 每秒測試一次
        time.sleep(1)

    print("Ping finished.")
