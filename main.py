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
from plot_rtt import plot_rtt_results

class BandwidthDelayTopo(Topo):
    def build(self):
        # Create hosts and servers
        h1 = self.addHost('h1', ip='140.115.154.245/24')        # Host1
        s1 = self.addHost('s1', ip='140.115.154.246/24')        # Server1
        s2 = self.addHost('s2', ip='140.115.154.247/24')        # Server2

        # Create Open vSwitch
        sw1 = self.addSwitch('sw1')                            # Switch1

        # Connect hosts and servers to the switch with specific link parameters
        self.addLink(h1, sw1, cls=TCLink, bw=10)
        self.addLink(s1, sw1, cls=TCLink, bw=10)
        self.addLink(s2, sw1, cls=TCLink, bw=10)



def start_network():
    # Create topology and start network
    topo = BandwidthDelayTopo()
    net = Mininet(topo=topo, controller=Controller, switch=OVSSwitch, link=TCLink)
    net.start()

    try:
        # Get hosts and servers
        h1 = net.get('h1')
        s1 = net.get('s1')
        s2 = net.get('s2')

        # 結果字典
        normal_rtt_results = {}
        abnormal_rtt_results = {}

        # 啟動正常流量執行緒
        print("\n=== Start S1 Normal Traffic ===")
        t1 = threading.Thread(target=normal_flow, args=(net, normal_rtt_results))
        t1.start()
        t1.join()  # 等待正常流量執行緒完成

        # 如果需要異常流量，可啟動異常流量執行緒
        # print("\n=== Start S2 Abnormal Traffic ===")
        # t2 = threading.Thread(target=abnormal_flow, args=(net, abnormal_rtt_results))
        # t2.start()
        # t2.join()

        # 檢查結果是否為空並繪圖
        if normal_rtt_results.get('ping_results'):
            print("\n=== Plotting RTT Results for Normal Traffic ===")
            plot_rtt_results(normal_rtt_results, title="RTT Over Time: Normal Traffic")
        else:
            print("No RTT results available for normal traffic.")

        # 如果需要處理異常流量結果
        # if abnormal_rtt_results.get('ping_results'):
        #     print("\n=== Plotting RTT Results for Abnormal Traffic ===")
        #     plot_rtt_results(abnormal_rtt_results, title="RTT Over Time: Abnormal Traffic")
        # else:
        #     print("No RTT results available for abnormal traffic.")

    finally:
        CLI(net)  # Optional: Allow user to manually interact with the network
        net.stop()

def main():
    start_network()

if __name__ == '__main__':
    main()