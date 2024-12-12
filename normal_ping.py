import time
import re

def normal_flow(net, normal_rtt_results):
    """
    執行正常流量：s1 每秒對 h1 執行一次 ping，將 RTT 結果儲存到 normal_rtt_results 中。
    
    :param net: Mininet 網路實例
    :param normal_rtt_results: 用於儲存 RTT 結果的字典
    """
    h1 = net.get('h1')
    s1 = net.get('s1')

    # 初始化 RTT 結果
    if 'ping_results' not in normal_rtt_results:
        normal_rtt_results['ping_results'] = []

    try:
        print("Starting normal flow: s1 pinging h1")
        while True:
            # 執行 ping 命令，指定封包大小為 64 字節
            ping_output = s1.cmd(f'ping -c 1 -s 64 {h1.IP()}')

            # 使用正則表達式提取 RTT
            match = re.search(r'time=(\d+\.\d+) ms', ping_output)
            if match:
                rtt = float(match.group(1))
                timestamp = time.strftime("%H:%M:%S", time.localtime())

                # 儲存 RTT 結果
                normal_rtt_results['ping_results'].append({
                    'timestamp': timestamp,
                    'rtt': rtt
                })

                print(f"[{timestamp}] Ping RTT: {rtt} ms")
            else:
                print("Ping failed or RTT not found")

            # 每秒執行一次 ping
            time.sleep(1)

    except KeyboardInterrupt:
        print("Normal flow interrupted by user.")
