from Package import Package
from MapGraph import DistanceTable
from datetime import datetime
from PackageTable import PackageTable
import csv
# Static class used to get package data and distance data from text files
class GetData:
    # Gets package data from text file
    # Big O: N - number of packages in text file
    def package_data_into_list():
        with open('package.csv') as csvfile:
            readCSV = csv.reader(csvfile, delimiter = ',')
            package_table = PackageTable()
            for row in readCSV:
                package = Package()
                package.set_id(int(row[0]))
                if package.get_id() == 9:
                    package.set_address("410 S State St")
                    package.set_city(row[2])
                    package.set_state(row[3])
                    package.set_zip("84111")
                else:
                    package.set_address(row[1])
                    package.set_city(row[2])
                    package.set_state(row[3])
                    package.set_zip(row[4])
                format = '%I:%M %p'  # Format for converting string to time class
                if row[5] == 'EOD':
                    deadline = 'EOD'
                else:
                    deadline = datetime.strptime(row[5],format).time()  # Converts to time class
                package.set_deadline(deadline)
                package.set_weight(int(row[6]))
                package.set_special(row[7])
                # Inserts package into package table
                package_table.insert_package(package)
            return package_table

    # Gets distance data from text file based on address as keys
    # Big O: N^2 - number of addresses in file
    def distance_into_table():
        with open('distanceTable.csv') as csvfile:
            readCSV = csv.reader(csvfile,delimiter = ',')
            map_graph = DistanceTable()
            for row in readCSV:
                address1 = row[0]
                map_graph.add_address(address1)
                distance_index = 1
                for address2 in map_graph.address_list:
                    map_graph.set_distance(address1,address2,row[distance_index])
                    distance_index += 1

        return map_graph