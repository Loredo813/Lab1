def monitor_ping_rtt(host_name, target_ip):
    with subprocess.Popen(['ping', target_ip], stdout=subprocess.PIPE, text=True) as process:
        for line in process.stdout:
            match = re.search(r'time=(\d+\.\d+) ms', line)
            if match:
                # 获取时间戳，格式为 HH:MM:SS.fff
                timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
                rtt = match.group(1)
                # 将数据写入CSV文件
                with open(csv_filename, 'a', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow([timestamp, host_name, rtt])
            time.sleep(0.001)  # 稍微等待，以减少CPU占用
