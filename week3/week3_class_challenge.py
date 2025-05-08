# 1. Write a loop to create a list of just the unique IP Addresses and display how many there are total in the log file.

new_list = []

with open("simplified-network-log.txt", "r") as file:
    header = file.readline()  # skip the header line
    for line in file:  # loop through the lines in file
        line = line.split(',')
        ip_address = line[1] # index of the ip addresses in the line
        if ip_address not in new_list:
            new_list.append(ip_address)

print(new_list)
print(f'Q1. There are {len(new_list)} unique IP addresses in simplified network.')



# 2.  Use datetime to show the first date and the last date from the log file, and the time difference between them (duration total)
from datetime import datetime

timestamps = []

# Read the file and extract timestamps
with open("simplified-network-log.txt", "r") as file:
    header = file.readline()  # Skip the header line
    for line in file:
        line = line.strip().split(',')
        timestamp = datetime.strptime(line[0], "%Y-%m-%d %H:%M:%S")  # Converts string to datetime
        timestamps.append(timestamp)

# Find the first and last timestamps
first_timestamp = min(timestamps)
last_timestamp = max(timestamps)
time_difference = last_timestamp - first_timestamp

# Display results
print(f"Q2. The first timestamp is: {first_timestamp}, the last timestamp is: {last_timestamp}, and the time difference is {time_difference}")


# 3.  Count the total rows/lines and print the total
count = 0
with open("simplified-network-log.txt", "r") as file:
    header = file.readline()
    for line in file:
        count = count + 1
print(f'Q3. There are {count} lines in simplified network log.txt.')



# 4.  Combine the data from inbound and outbound, how much data was sent total within the log file?
total_data_sent = 0
with open("simplified-network-log.txt", "r") as file:
    header = file.readline()
    for line in file:
        line = line.strip().split(',')
        data_sent = int(line[3])  # extract data size in KB
        total_data_sent += data_sent  # sum up the data

print(f'Q4. The total data sent within the log file is {total_data_sent} combining data from inbound and outbound.')



# 5.  How much data was sent via inbound traffic vs. outbound traffic?  WHich one has more?
print("Q5.")

inbound_data = 0
outbound_data = 0

with open("simplified-network-log.txt", "r") as file:
    header = file.readline()
    for line in file:
        line = line.strip().split(',')
        traffic_type = line[2]  # extract whether the traffic (action) is inbound or outbound
        data_size = int(line[3])  # get the data size in KB

        if traffic_type == "inbound":
            inbound_data += data_size
            print(f"Inbound Data Sent: {inbound_data} KB")
        elif traffic_type == "outbound":
            outbound_data += data_size
            print(f"Outbound Data Sent: {outbound_data} KB")


# Check which traffic type has more data
if inbound_data > outbound_data:
    higher_traffic_type = "Inbound"
elif outbound_data > inbound_data:
    higher_traffic_type = "Outbound"
else:
    higher_traffic_type = "Equal"
    print("Inbound and Outbound traffic have equal data transfer.")

print(f"The higher traffic type is: {higher_traffic_type}")

# 6.  What is the most active IP address by activity count and by total data sent/received?
print("Q6.")
ip_activity_count = {}  # to store IP addresses as keys and their occurrence counts as values
ip_data_usage = {}  # to store IP addresses as keys and their data as values

with open("simplified-network-log.txt", "r") as file:
    header = file.readline()
    for line in file:
        line = line.strip().split(',')
        ip_address = line[1]  # extract IP address
        data_size = int(line[3])  # data size in KB

        # count occurrences of each IP address
        if ip_address in ip_activity_count:
            ip_activity_count[ip_address] += 1
        else:
            ip_activity_count[ip_address] = 1

        # sum total data transferred by each IP
        if ip_address in ip_data_usage:
            ip_data_usage[ip_address] += data_size
        else:
            ip_data_usage[ip_address] = data_size

# Find the most active IP by count
most_active_ip_address = max(ip_activity_count, key=ip_activity_count.get) # IP address with the highest count
most_active_ip_count = ip_activity_count[most_active_ip_address] # retrieve the count for that IP

# find the IP with the most data transferred
most_data_ip_address = max(ip_data_usage, key=ip_data_usage.get) # get the IP with the highest total data
most_data_ip_count = ip_data_usage[most_data_ip_address] # retrieve the total data transferred

print(f"Most Active IP (by count): {most_active_ip_address} with {most_active_ip_count} occurrences")
print(f"Most Data Transferred IP: {most_data_ip_address} with {most_data_ip_count} KB transferred")


