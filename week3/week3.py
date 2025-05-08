# importing

# open()  header =  # open is used "with"
# with open("simplified-network-log.txt", "r") as file:
#     #header = file.readline()
#     #print(header)
#     for line in file:
#      #print(line.strip()) # the strip gets rid of the white spaces in between the lines
#        line =

# creating new lists for unique values or separates data sets

new_list = []

with open("simplified-network-log.txt", "r") as file:
    header = file.readline()
    for line in file:
        line = line.split(',')
        ip_address = line[1]
        if ip_address not in new_list:
            new_list.append(ip_address)

print(new_list)
print(f'There are {len(new_list)} new IP addresses in simplified network.')

# import csv

# split logs/text

