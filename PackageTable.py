from Package import Package
# Package Table class used to hold daily packages using chain double hashing
# Chain Hashing is used to hold packages going to the same address are stored
# Double Hashing is used to prevent different address from ending up in the same bucket

# Class for an empty bucket
class EmptyBucket:
    pass
class PackageTable:
    #Constructor
    def __init__(self,length = 41 ):
        # Initialize list for hash
        self.address_table = []

        # Initialize the list for id hash table
        self.id_hash_table = []

        # Zip table holds the id for all packages based on zip code
        # Zip list is prepopulated from Map for closest next zip
        # Could be done in code if zip distance table was provided
        self.zip_table = [['84107'],['84121'],['84117'],['84115'],['84106'],['84105'],
                          ['84111'],['84103'],['84104'],['84119'],['84118'],['84123'],['10:30']]
        # Holds daily package ids for printing
        self.package_ids = []

        # Current zip code holds the location of
        self.current_zip_code = 12

        # Current and length are used for itteration and length overrides
        self.current = -1
        self.length = length

        # Constrants for empty cells
        self.EMPTY_SINCE_START = EmptyBucket()
        self.EMPTY_AFTER_REMOVAL = EmptyBucket()

        # Initalize address_table cells to be EMPTY_SINCE_START
        # Initalize id_hash_table to none
        for i in range(length):
            temp = [self.EMPTY_SINCE_START]
            self.address_table.append(temp)
            self.id_hash_table.append(None)

    def __iter__(self):
        return self

    def __next__(self):
        self.current += 1
        if self.current < self.length:
            return self.address_table[self.current]
        raise StopIteration

    def __len__(self):
        return len(self.address_table)


    # Primary hash fuction can be used for zip or address hashing
    # Big O: N - number of packages in table
    def hash_1_address(self, address):
        for i in range(self.length):
            # Calculate bucket index for the package for this value of i
            # Hash() is used for h1 and hash_2 is used for h2
            bucket = (hash(address) + self.hash_2_address(address) * i) % len(self.address_table)
            bucket_list = self.address_table[bucket]

            # Returns Bucket index if an emptybucket or
            # if package shares the exact address
            if type(bucket_list[0]) is EmptyBucket:
                return bucket
            elif bucket_list[0].get_address() == address:
                return bucket

        # Returns false if cant find empty bucket
        return False


    # Secondary hash function
    def hash_2_address(self, item):
        return 7 - hash(item) % 7


    # Hash fuction based on id.
    def get_hash_bucket_by_id(self, id):
        return hash(id) % self.length

    # Returns address based of id
    def get_address(self,id):
        package = self.get_package(id)
        return package.get_address()

    # Inserts a new package into the hash table based address
    # Updates the id hash list with correct index of address hash
    # Big O: N  -the amount of zip codes
    def insert_package(self,package):
        # Get correct list based on address code
        bucket = self.hash_1_address(package.get_address())
        bucket_list = self.address_table[bucket]
        self.package_ids.append(package.get_id())
        # Chains if the address is the same
        if (type(bucket_list[0])) is EmptyBucket:
            bucket_list[0] = package
        else:
            bucket_list.append(package)

        # Adds the address hash buck to id_hash_table based on a hashed id
        self.id_hash_table[self.get_hash_bucket_by_id(package.get_id())]= bucket
        # Inserts package id into zip table based on packages zip code
        if package.get_deadline() != 'EOD':
            self.zip_table[12].append(package.get_id())
        else:
            for zip in self.zip_table:
                if zip[0] == package.get_zip():
                    zip.append(package.get_id())
                    break
    # Returns package based on id
    # Big O: N - number of packages in address chain
    def get_package(self, id):
        bucket = self.address_table[self.id_hash_table[self.get_hash_bucket_by_id(id)]]
        for package in bucket:
            if package.get_id() == id:
                return package
    # Prints all packages by calling the print_package funtion in the package class
    def print_all_packages(self,time):
        for id in self.package_ids:
            self.get_package(id).print_package(time)