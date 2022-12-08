# Dictonery used to hold distance table based on address
# DistanceTable object used to hold all distances

class DistanceTable:
    # Constructor
    def __init__(self):
        self.address_list = []
        self.distance = {}
    # Stores previous used address to use for dict keys
    def add_address(self, address):
        self.address_list.append(address)
    # Getters and setters for distance table
    def set_distance(self, address1, address2, distance):
        self.distance[address1, address2] = distance
        self.distance[address2, address1] = distance

    def get_distance(self, address1, address2):
        return self.distance[address1, address2]