# C950 - Data Structure and Algorithm II
# Student ID: 011672297
# Name: Tuan Dat Doan
import csv
import datetime
import math

from HashMap import HashTable
from Address import Address
from Package import Package
from Truck import Truck

# Create a variable to store current time
time = datetime.timedelta(hours=23, minutes=59)

# Create Hashtable for Packages
package_HT = HashTable(40)
# Load packages into hash table:
file = open('Package_File.csv')
packages = csv.reader(file)
packages = list(packages)
for package in packages:
    p_id = int(package[0])
    p_address = package[1]
    p_city = package[2]
    p_state = package[3]
    p_zipcode = package[4]
    p_deadline = package[5]
    p_weight = int(package[6].split(" ")[0])

    p = Package(p_id, p_address, p_deadline, p_city, p_state, p_zipcode, p_weight, "At the hub")
    package_HT.insert(p_id, p)

# Create hash table for Addresses
address_HT = HashTable(27)
# Load addresses into hash table
file = open('Address_File.csv')
addresses = csv.reader(file)
addresses = list(addresses)
for address in addresses:
    a_id = int(address[0])
    a_name = address[1]
    a_address = address[2]
    a = Address(a_id, a_name, a_address)
    address_HT.insert(a_address, a)


# Function to find the sequence of delivery using nearest neighbor algorithm
def WGUPS(delivery_addresses, truck):
    # The truck starts at the service hub
    start = '4001 South 700 East'
    visited_addresses = []
    unvisited_addresses = delivery_addresses
    current_address_id = address_HT.get(start).id
    visited_addresses.append(current_address_id)

    # Nearest neighbor algorithm
    while len(unvisited_addresses) > 0:
        next_address_id = current_address_id
        # dummy value to compare with the shortest route
        shortest_route = 10000000

        # Find the address that has the shortest route to current address
        for e in unvisited_addresses:
            # skip packages that had the same addresses with shipped packages as they can be shipped together
            if e in visited_addresses:
                continue
            else:
                # Find distance between 2 addresses
                file = open('Distance_File.csv')
                distances = csv.reader(file)
                distances = list(distances)
                distance = distances[current_address_id][e]
                if distance == '':
                    distance = distances[e][current_address_id]
                # If distance is shortest, mark 'a' as next delivery address
                if float(distance) < float(shortest_route):
                    shortest_route = float(distance)
                    next_address_id = e

        # Mark next address as current address for next loop, and remove it from unvisited list
        visited_addresses.append(next_address_id)
        unvisited_addresses.remove(next_address_id)
        current_address_id = next_address_id

        # Document time and distance travel on object Truck
        truck.mileage += shortest_route
        travelled_time = shortest_route / 18
        minute = (travelled_time - math.floor(travelled_time)) * 60
        hour = math.floor(travelled_time)
        truck.end_time += datetime.timedelta(hours=hour, minutes=minute)

        # Document the package with departure time and delivered time
        for package_id in truck.packages:
            p = package_HT.get(package_id)
            p_address_id = address_HT.get(p.address).id
            if p_address_id == next_address_id:
                p.start_time = truck.start_time
                p.end_time = truck.end_time
                p.truck_id = truck.id
            else:
                continue

    # After all the packages are delivered, the truck must return to the hub
    visited_addresses.append(address_HT.get(start).id)


# A lookup function that takes the package ID as input
# and returns delivery address, deadline, city, zipcode, weight, and delivery status
def lookupSpecificPackage(packageID):
    if packageID == 9:
        if time >= datetime.timedelta(hours=10, minutes=20):
            package_HT.get(9).address = "410 S State St"
        else:
            package_HT.get(9).address = "300 State St"
    p = package_HT.get(packageID)
    if p.start_time < time:
        p.status = "Delivered"
    elif p.start_time > time > p.end_time:
        p.status = "En route"
    else:
        p.status = "At the hub"
    return str(p)


# A lookup function to look up specific packages at specific time
def lookupPackages():
    if (time == datetime.timedelta(hours=23, minutes=59)):
        print("Status of packages at EOD")
    else:
        print("Status of packages at " + str(time))
    print("--------------------------")
    for p in range(1, 41):
        print(lookupSpecificPackage(p))
        print()


def main():
    # Load packages that need to be delivered before 10:30 on truck 1
    packages_1 = [1, 13, 14, 15, 16, 19, 20, 29, 30, 31, 34, 37, 40]
    # Get all the delivery addresses from above package
    addresses_1 = set()
    for package_id in packages_1:
        p = package_HT.get(package_id)
        a = address_HT.get(p.address)
        addresses_1.add(a.id)
    truck_1 = Truck(1, packages_1, 0.0, datetime.timedelta(hours=8))
    # Find the shortest routes and update expected departure time and ETA for packages on truck 3
    WGUPS(addresses_1, truck_1)

    # Load packages that are delayed until 9:05 on truck 2 with packages that can only be on truck 2,
    # plus random packages to meet the capacity of 16
    packages_2 = [3, 6, 18, 25, 28, 32, 36, 38, 2, 4, 5, 7, 8, 10, 11, 12]
    # Get all the delivery addresses from above package
    addresses_2 = set()
    for package_id in packages_2:
        p = package_HT.get(package_id)
        a = address_HT.get(p.address)
        addresses_2.add(a.id)
    truck_2 = Truck(1, packages_2, 0.0, datetime.timedelta(hours=9, minutes=5))
    # Find the shortest routes and update expected departure time and ETA for packages on truck 3
    WGUPS(addresses_2, truck_2)

    # Load packages that have the wrong addresses which can only be fixed at 10:20 and the remaining packages
    packages_3 = [9, 17, 19, 21, 22, 23, 24, 26, 27, 33, 35, 39]
    # Get all the delivery addresses from above package
    addresses_3 = set()
    for package_id in packages_3:
        p = package_HT.get(package_id)
        a = address_HT.get(p.address)
        addresses_3.add(a.id)
    truck_3 = Truck(1, packages_3, 0.0, datetime.timedelta(hours=10, minutes=20))
    # While expected departure is 10:20, if the driver from truck 1 or 2 gets back to the hub later,
    # the departure time would be delayed
    possible_start = min(truck_1.end_time, truck_2.end_time)
    if possible_start > truck_3.start_time:
        truck_3.start_time = possible_start
    # Find the shortest routes and update expected departure time and ETA for packages on truck 3
    WGUPS(addresses_3, truck_3)

    # Mark variable time as global to be updated and used in other functions
    global time

    i = 0
    while i != "4":
        i = input("Possible Menu Options:"
            + "\n***************************************"
            + "\n1. Print All Package Status and Total Mileage"
            + "\n2. Get a Single Package Status with a Time"
            + "\n3. Get All Package Status with a Time"
            + "\n4. Exit the Program"
            + "\n***************************************"
            + "\nPlease enter a number: ")
        if i == "1":
            time = datetime.timedelta(hours=23, minutes=59)
            lookupPackages()
            print("Total Mileage:" + str(truck_1.mileage + truck_2.mileage + truck_3.mileage))
        elif i == "2":
            time_input = input("Please enter a time (Format HH:MM): ")
            time = datetime.timedelta(hours=int(time_input.split(":")[0]), minutes=int(time_input.split(":")[1]))
            ID = input("Please enter a package ID (1-40): ")
            print(lookupSpecificPackage(int(ID)))
        elif i == "3":
            time_input = input("Please enter a time (Format HH:MM): ")
            time = datetime.timedelta(hours=int(time_input.split(":")[0]), minutes=int(time_input.split(":")[1]))
            lookupPackages()
        print("\n----------------------------------\n")


if __name__ == '__main__':
    main()
