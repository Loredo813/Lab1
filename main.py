from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSSwitch, Controller
from mininet.link import TCLink
from mininet.cli import CLI
import threading
import time
from normal_ping import normal_flow
from abnormal_ping import abnormal_flow
from plot_rtt import plot_rtt_results
from statsic import calculate_rtt_statistics


class BandwidthDelayTopo(Topo):
    def build(self):
        # Create hosts and servers
        h1 = self.addHost('h1', ip='140.115.154.245/24')  # Host1
        s1 = self.addHost('s1', ip='140.115.154.246/24')  # Server1
        s2 = self.addHost('s2', ip='140.115.154.247/24')  # Server2

        # Create Open vSwitch
        sw1 = self.addSwitch('sw1')  # Switch1

        # Connect hosts and servers to the switch with specific link parameters
        self.addLink(h1, sw1, cls=TCLink, bw=10)
        self.addLink(s1, sw1, cls=TCLink, bw=10)
        self.addLink(s2, sw1, cls=TCLink, bw=10)


def configure_bandwidth(net, option):
    """
    Configure the bandwidth of the switch interface based on the selected option.
    """
    h1 = net.get('h1')
    sw1 = net.get('sw1')

    # Determine bandwidth limits based on the option
    if option == 1:
        print("Configuring bandwidth: 5Mbps to s1 and 5Mbps to s2.")
        sw1.cmd('ovs-vsctl set interface s1 ingress_policing_rate=5000')
        sw1.cmd('ovs-vsctl set interface s2 ingress_policing_rate=5000')
    elif option == 2:
        print("Configuring bandwidth: 7Mbps to s1 and 3Mbps to s2.")
        sw1.cmd('ovs-vsctl set interface s1 ingress_policing_rate=7000')
        sw1.cmd('ovs-vsctl set interface s2 ingress_policing_rate=3000')
    elif option == 3:
        print("Configuring bandwidth: 10Mbps total.")
        sw1.cmd('ovs-vsctl set interface s1 ingress_policing_rate=10000')
        sw1.cmd('ovs-vsctl set interface s2 ingress_policing_rate=10000')
    else:
        print("Invalid option. Keeping default bandwidth.")


def run_experiment(net):
    """
    Run normal and abnormal flow experiments.
    """
    print("Starting normal and abnormal flow experiments...")
    normal_rtt_results = []
    abnormal_rtt_results = []

    normal_thread = threading.Thread(target=normal_flow, args=(net, normal_rtt_results))
    abnormal_thread = threading.Thread(target=abnormal_flow, args=(net, abnormal_rtt_results))

    normal_thread.start()
    time.sleep(5)
    abnormal_thread.start()

    normal_thread.join()
    abnormal_thread.join()

    print("Calculating and plotting RTT statistics...")
    normal_stat = calculate_rtt_statistics(normal_rtt_results)
    if normal_stat:
        print("Normal RTT Statistics:")
        print(f"  Average RTT: {normal_stat['average']} ms")
        print(f"  Minimum RTT: {normal_stat['min']} ms")
        print(f"  Maximum RTT: {normal_stat['max']} ms")
        print(f"  Standard Deviation: {normal_stat['std_deviation']} ms")

    plot_rtt_results(normal_rtt_results, title="Normal RTT Over Time")

    abnormal_stat = calculate_rtt_statistics(abnormal_rtt_results)
    if abnormal_stat:
        print("Abnormal RTT Statistics:")
        print(f"  Average RTT: {abnormal_stat['average']} ms")
        print(f"  Minimum RTT: {abnormal_stat['min']} ms")
        print(f"  Maximum RTT: {abnormal_stat['max']} ms")
        print(f"  Standard Deviation: {abnormal_stat['std_deviation']} ms")

    plot_rtt_results(abnormal_rtt_results, title="Abnormal RTT Over Time")
    print("Experiment completed.")


def start_network():
    """
    Start the network and provide CLI commands to run experiments with dynamic bandwidth configuration.
    """
    topo = BandwidthDelayTopo()
    net = Mininet(topo=topo, controller=Controller, switch=OVSSwitch, link=TCLink)
    net.start()

    print("Network started. Use the CLI to configure and run experiments.")

    def run_with_config():
        print("Select bandwidth configuration:")
        print("1: Split 5Mbps:5Mbps (Total 10Mbps)")
        print("2: Split 7Mbps:3Mbps (Total 10Mbps)")
        print("3: Maintain 10Mbps default")
        option = int(input("Enter option (1/2/3): "))
        configure_bandwidth(net, option)
        run_experiment(net)

    CLI.do_run_experiment = lambda self, line: run_with_config()

    try:
        CLI(net)
    finally:
        print("Stopping network...")
        net.stop()


def main():
    start_network()


if __name__ == '__main__':
    main()
