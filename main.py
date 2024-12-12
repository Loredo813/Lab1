from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSSwitch, Controller, Host
from mininet.link import TCLink
from mininet.cli import CLI
import time
import matplotlib.pyplot as plt
import re
import threading
from normal_ping import normal_flow
from abnormal_ping import abnormal_flow
from plot_rtt import plot_rtt_comparison
from statsic import calculate_rtt_statistics

class BandwidthDelayTopo(Topo):
    def build(self):
        # Create hosts and servers
        h1 = self.addHost('h1', ip='140.115.154.245/24')        # Host1
        s1 = self.addHost('s1', ip='140.115.154.246/24')        # Server1
        s2 = self.addHost('s2', ip='140.115.154.247/24')        # Server2

        # Create Open vSwitch
        sw1 = self.addSwitch('sw1')                            # Switch1

        # Connect hosts and servers to the switch with specific link parameters
        self.addLink(h1, sw1, cls=TCLink, bw=10,delay=5)
        self.addLink(s1, sw1, cls=TCLink, bw=10,delay=5)
        self.addLink(s2, sw1, cls=TCLink, bw=10,delay=5)



def start_network():
    # Create topology and start network
    topo = BandwidthDelayTopo()
    net = Mininet(topo=topo, controller=Controller, switch=OVSSwitch, link=TCLink)
    net.start()

    try:

        # 結果字典
        normal_rtt_results = {}
        abnormal_rtt_results = {}

        # 啟動正常流量執行緒
        print("\n=== Start S1 Normal Traffic ===")
        t1 = threading.Thread(target=normal_flow, args=(net, normal_rtt_results))
        t1.start()

        time.sleep(5)# 延遲 5 秒
        print("\n=== Start S2 Abnormal Traffic ===")
        t2 = threading.Thread(target=abnormal_flow, args=(net, abnormal_rtt_results))
        t2.start()

        # 等待兩個執行緒都完成
        t1.join()
        t2.join()
        print("\n=== All Traffic Completed ===")


        
        stats = calculate_rtt_statistics( normal_rtt_results)
        if stats:
            print(f"S1 RTT Statistics:")
            print(f"  Average RTT: {stats['average']} ms")
            print(f"  Maximum RTT: {stats['max']} ms")
            print(f"  Minimum RTT: {stats['min']} ms")
            print(f"  Standard Deviation: {stats['std_deviation']} ms")
        else:
            print("No RTT data available.")




        ab_stats = calculate_rtt_statistics(abnormal_rtt_results)
        if ab_stats:
            print(f"S2 RTT Statistics:")
            print(f"  Average RTT: {ab_stats['average']} ms")
            print(f"  Maximum RTT: {ab_stats['max']} ms")
            print(f"  Minimum RTT: {ab_stats['min']} ms")
            print(f"  Standard Deviation: {ab_stats['std_deviation']} ms")
        else:
            print("No RTT data available.")

        # 如果需要處理兩種流量的結果
        if normal_rtt_results.get('ping_results') or abnormal_rtt_results.get('ping_results'):
            print("\n=== Plotting RTT Results for Both Normal and Abnormal Traffic ===")
            plot_rtt_comparison(normal_rtt_results, abnormal_rtt_results)
        else:
            print("No RTT results available for plotting.")



    finally:
        CLI(net)  # Optional: Allow user to manually interact with the network
        net.stop()

def main():
    start_network()

if __name__ == '__main__':
    main()