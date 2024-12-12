import time
import re

def abnormal_flow(net, abnormal_rtt_results):
    h1 = net.get('h1')
    s2 = net.get('s2')

    # 初始化結果字典
    abnormal_rtt_results.setdefault('ping_results', [])
    start_time = time.time()
    end_time = start_time + 10


    while time.time() < end_time:
        # 單次 Ping
        s2result = s2.cmd(f'ping -c 1 -s 1024 -W 1 {h1.IP()}')
        
        # 匹配 RTT
        rtt_pattern = re.compile(r'time=([\d\.]+) ms')
        match = rtt_pattern.search(s2result)

        # 紀錄結果
        current_time = time.strftime('%H:%M:%S', time.localtime())
        if match:
            rtt = round(float(match.group(1)), 2)
            abnormal_rtt_results['ping_results'].append({
                'source': s2.name,
                'target': h1.name,
                'rtt': rtt,
                'timestamp': time.time() - start_time  # 記錄相對於啟動時間的時間戳
            })
            print(f"[{current_time}] Success: RTT={rtt} ms (Source: {s2.name}, Target: {h1.name})")
        else:
            print(f"[{current_time}] Ping failed: No RTT recorded (Source: {s2.name}, Target: {h1.name})")
        
        # 每秒測試一次
        time.sleep(0.004)

    print("Ping finished.")