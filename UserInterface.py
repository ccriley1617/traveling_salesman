from Package import Package
from PackageTable import PackageTable
from datetime import datetime
# Static class used to run user interface
class UserInterface:
    # Runs the user interface
    def user_interface(self, table):
        # Gets input time from user and prints all package information for that time
        # Try catch is for incorrect user data entry
        # Big O: N - number of user inquiries
        while True:
            try:
                print("Enter time for package Status Check in Military Time ex: 8:00, 10:15, 13:30, 17:00")
                print("'E' to exit program")
                print("Time:")
                string_time = input()
                if string_time == 'E':
                    return True
                string_time = string_time.split(':')
                time = datetime(1, 1, 1, int(string_time[0]), int(string_time[1]))
                table.print_all_packages(time.time())
            except:
                print("Input Incorrect")





