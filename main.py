# Conor Riley
from Package import Package
from PackageTable import PackageTable
from GetData import GetData
from TruckClass import TruckClass
from MapGraph import DistanceTable
from UserInterface import UserInterface
import csv

# Get Data From Text files
table = GetData.package_data_into_list()
map_graph = GetData.distance_into_table()

#Generate truck objects
truck1 = TruckClass()
truck2 = TruckClass()
truck3 = TruckClass()
#Load special packages. Ones with deadlines or special instructions
truck1.load_special_packages(table, truck2, truck3)
#Load trucks to capacity
truck1.load_truck_by_zip(table)
truck2.load_truck_by_zip(table)
truck3.load_truck_by_zip(table)
#Generate the fastest routes for the two trucks
truck1.nine_deadline(table, map_graph)
truck2.generate_fastest_route(table, map_graph)
#Send first two trucks out. Truck1 has the deadlined deliveries
truck1.deliver_packages(table, map_graph,1)
truck2.deliver_packages(table, map_graph,2)
#Reload Truck 1 and give Truck three to driver of truck2
#Generates fastest route
truck1.load_truck_by_zip(table)
truck1.generate_fastest_route(table, map_graph)
truck3.generate_fastest_route(table, map_graph)
truck3.set_truck_time(truck2.get_truck_time())
#Send last two trucks out
truck3.deliver_packages(table, map_graph,3)
truck1.deliver_packages(table, map_graph,1)

print("Total mileage:", truck1.get_truck_mileage() + truck2.get_truck_mileage() + truck3.get_truck_mileage())
#Calls user interface
user = UserInterface()
user.user_interface(table)