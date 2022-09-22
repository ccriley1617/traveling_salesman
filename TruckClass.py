from PackageTable import PackageTable
from datetime import datetime, timedelta
from MapGraph import DistanceTable
# Truck Class that creates Truck object
class TruckClass:

    def __init__(self):
        # Initialize list for packages on truck
        # Current and length are used for itteration and length overrides
        # Truck_package_count
        self.truck_packages = []
        self.truck_mileage = 0.0
        format = '%I:%M %p'  # Format for converting string to time class
        self.truck_time = datetime(1,1,1,8)
        self.current = -1
        self.length = 10

    def __iter__(self):
        return self

    def __next__(self):
        self.current += 1
        if self.current < self.length:
            return self.truck_packages[self.current]
        raise StopIteration

    def __len__(self):
        return len(self.truck_packages)

    # Getters and setters for truck_time and mileage
    def set_truck_time(self, time):
        self.truck_time = time

    def get_truck_time(self):
        return self.truck_time

    def get_truck_mileage(self):
        return self.truck_mileage

    # Pops a specific package from a list in the zip table based on the packages ID
    # Used for the deadline deliveries and the special instrution packages
    # Big O: N - number of packages in zip_table
    def pop_package_from_zip_table(self,zip_table,package_id):
        index = 1
        while index < len(zip_table):
            if zip_table[index] == package_id:
                return zip_table.pop(index)
            index += 1

    # Loads special packages with deadlines or instructions. If statements could be used for deadline's and
    # if there were codes for the special instrutions the loading of those could be automated as well.
    def load_special_packages(self,package_table, truck2, truck3):
        self.truck_packages.append(self.pop_package_from_zip_table(package_table.zip_table[3], 19))
        truck2.truck_packages.append(self.pop_package_from_zip_table(package_table.zip_table[7], 3))
        truck2.truck_packages.append(self.pop_package_from_zip_table(package_table.zip_table[11], 18))
        truck2.truck_packages.append(self.pop_package_from_zip_table(package_table.zip_table[9], 36))
        truck2.truck_packages.append(self.pop_package_from_zip_table(package_table.zip_table[6], 38))
        truck3.truck_packages.append(self.pop_package_from_zip_table(package_table.zip_table[12],6))
        truck3.truck_packages.append(self.pop_package_from_zip_table(package_table.zip_table[12],25))
        truck3.truck_packages.append(self.pop_package_from_zip_table(package_table.zip_table[3], 28))
        truck3.truck_packages.append(self.pop_package_from_zip_table(package_table.zip_table[9], 32))
        truck3.truck_packages.append(self.pop_package_from_zip_table(package_table.zip_table[6], 9))


    # Loads the remaining packages based on the zip code. Once the current zip's packages are zero moves on to
    # the next closest geographical zip code.
    # Big O: N^2 - number of packages if every one goes to different zip code
    def load_truck_by_zip(self,package_table):
        while (package_table.current_zip_code >= 0):
            while (len(package_table.zip_table[package_table.current_zip_code]) > 1) and (
                    len(self.truck_packages) < self.length):
                self.truck_packages.append(package_table.zip_table[package_table.current_zip_code].pop(1))
            if (len(self.truck_packages) == self.length) or (
                    package_table.current_zip_code == len(package_table.zip_table)):
                return True
            package_table.current_zip_code -= 1
        else:
            return False

    # Haldles the on nine a.m. deadline package could be automated
    # Removes nine a.m package from list. Generates all possible routes for remaining packages and then
    # Adds the deadlined package to the front of the list for first delivery once truck leaves
    # Big O: N!*N^2 - number of packages on truck. Function itself is N but calls generate_fastest_route which is N!*N
    def nine_deadline(self,package_list, map_graph):
        index = 0
        while index < len(self.truck_packages):
            if self.truck_packages[index] == 15:
                id = self.truck_packages.pop(index)
                break
            index += 1
        self.generate_fastest_route(package_list,map_graph,package_list.get_address(id))
        self.truck_packages = [id] + self.truck_packages

    # Returns all permatations of the address list
    # Uses recusion to generate all permutations
    # Big O space complexity is is a constant because of use of a generator
    # Big O time Complexity: N! - number of addresses in list
    def get_package_list_permutations(self,address_list):
        # Handles the two base cases
        if len(address_list) == 0:
            yield []
        elif len(address_list) == 1:
            yield address_list
        # Removes item from list then splices list back together and recusively calls fuction again
        else:
            for i in range(len(address_list)):
                address = address_list[i]
                temp_address_list = address_list[:i] + address_list[i+1:]
                for permutation in self.get_package_list_permutations(temp_address_list):
                    yield [address] + permutation

    # Generates the fastest route for packeges to be delivered based on brute
    # force method
    # Uses hub as starting point for general use. Can be changed for the nine a.m package
    # Big O space complexity: N - number of packages generator is a constant
    # Big O time complexity: N!*N
    def generate_fastest_route(self, package_list, map_graph, starting_location = 'HUB'):
        # Get all address based on id
        address_list = []
        for id in self.truck_packages:
            address = package_list.get_address(id)
            if not( address in address_list):
                address_list.append(address)
        # Get all permutation of addresses
        permutation_address_list = self.get_package_list_permutations(address_list)
        # min_index stores index of smallest route known route
        # min_distance is the smallest distance found so far
        min_route = []
        min_distance = float("inf")
        # Check all permutations for the shortest total distance and returns that permutations
        for permutation in permutation_address_list:
            route_distance = 0.0
            # The starting and ending postion are alwasy the HUB
            permutation = [starting_location] + permutation + ['HUB']
            for i in range(len(permutation) -1):
                address1 = permutation[i]
                address2 = permutation[i+1]
                route_distance += float(map_graph.get_distance(address1,address2))

            if route_distance < min_distance:
                min_distance = route_distance
                min_route = permutation
        # Removes HUB destionations on list
        min_route.pop(0)
        min_route.pop()
        min_id_route = []
        # Converts address back in to ID numbers
        for address in min_route:
            for id in self.truck_packages:
                if package_list.get_address(id) == address:
                    min_id_route.append(id)
        self.truck_packages = min_id_route

    # Delivers all packages on the truck while updating mileage and time for the given truck
    # Big O: N - number of packages on truck
    def deliver_packages(self, package_list, map_graph,truck_number):
        # Applies the current time of the truck to all the packages left_hub_time varible on the truck
        for id in self.truck_packages:
            package = package_list.get_package(id)
            package.set_truck_number(truck_number)
            package.set_left_hub_time(self.get_truck_time())
        # Every truck starts at the hub
        address1 = "HUB"
        package_id = self.truck_packages.pop(0)
        package = package_list.get_package(package_id)
        address2 = package.get_address()
        self.deliver_package(address1,address2,package,map_graph,truck_number)
        # Delivers remaining packages while updating mileage and time
        while len(self.truck_packages) > 0:
            package_id = self.truck_packages.pop(0)
            address1 = package.get_address()
            package = package_list.get_package(package_id)
            address2 = package.get_address()
            self.deliver_package(address1,address2,package,map_graph,truck_number)
        # Returns truck to hub and applies correct mileage and time to truck varibles
        miles = float(map_graph.get_distance(address2, 'HUB'))
        self.truck_mileage += miles
        time_driving = timedelta(minutes=(3.3333333333333 * miles))
        self.truck_time = self.truck_time + time_driving

    # Delivers individual package and updates the trucks time and mileage
    def deliver_package(self,address1,address2,package, map_graph,truck_number):
        miles = float(map_graph.get_distance(address1, address2))
        self.truck_mileage += miles
        time_driving = timedelta(minutes=(3.3333333333333 * miles))
        self.truck_time = self.truck_time + time_driving
        package.set_delivered_time(self.truck_time)


