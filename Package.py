from datetime import datetime
# Package Class for package object
# Holds all package information for indivdual packages
class Package:
    # Constructor
    def __init__(self):
        # Records for delivery
        left_hub_time = False
        delivered_time = False
        truck_number = False
    # Setters for all package information
    def set_id(self, id):
        self.id = id

    def set_address(self, address):
        self.address = address

    def set_deadline(self, deadline):
        self.deadline = deadline

    def set_city(self, city):
        self.city = city

    def set_zip(self, zip):
        self.zip = zip

    def set_weight(self, weight):
        self.weight = weight

    def set_left_hub_time(self, left_hub_time):
        self.left_hub_time = left_hub_time

    def set_delivered_time(self,delivered_time):
        self.delivered_time = delivered_time

    def set_truck_number(self,number):
        self.truck_number = number

    def set_state(self,state):
        self.state = state

    def set_special(self,special):
        self.special = special
    #Getters for required information needed in program.
    def get_id(self):
        return self.id

    def get_address(self):
        return self.address

    def get_zip(self):
        return self.zip

    def get_deadline(self):
        return self.deadline

    # Prints package data in readable form based on a time of day
    def print_package(self, time = datetime(1,1,1,17).time()):
        # Checks for packages at hub
        if time < self.left_hub_time.time():
            print("ID:", self.id, "Address:", self.address, self.city, self.state, self.zip,"Deadline:", self.deadline,
                  "Special Instructions:", self.special, "Status: At Hub")
        # Checks for packages on truck
        elif time < self.delivered_time.time():
            print("ID:", self.id, "Address:", self.address, self.city, self.state, self.zip,"Deadline:", self.deadline,
                  "Special Instructions:", self.special, "Left Hub at:",
                  self.left_hub_time.time(), "Status: On Truck #", self.truck_number)
        # Prints all information for delivered package
        else:
            print("ID:", self.id, "Address:", self.address, self.city, self.state, self.zip, "Left Hub at:",
              self.left_hub_time.time(), "On Truck:", self.truck_number, "Delivered At:", self.delivered_time.time(),
              "Deadline:", self.deadline, "Special Instructions:", self.special, "Status: Delivered")