import datetime
import os

"""
Class campaign -
    Consists the list of campaign objects, methods for controlling campaigns
        - getter and setter methods of id, status and dayparting schedule
        - adding new campaigns
        - displaying on screen
        - saving and reading from file "campaign.txt"
"""
class Campaign:
    __campaigns = []
    __FILE_NAME = "campaign.txt"
    def __init__(self, id, brand_id, is_active=True, dayparting_hours=None):
        self.id = id
        self.brand_id = brand_id
        self.is_active = is_active
        self.dayparting_hours = dayparting_hours  # Tuple like (start_hour, end_hour)
    
    """ Getter method for id """
    def get_id(self):
        return self.id
    
    """ Getter method for brand id """
    def get_brand_id(self):
        return self.brand_id
    
    """ Getter method for campaign status """
    def get_active_status(self):
        return self.is_active
    
    """ Setter method for campaign status to turn on/off """
    def set_active_status(self, status):
        self.is_active = status
    
    """ Getter method for dayparting schedule: returns (hour, hour) or None """
    def get_dayparting_schedule(self):
        return self.dayparting_hours
    
    """ Getter class method for file name """
    @classmethod
    def get_file_name(cls):
        return cls.__FILE_NAME
    
    """ Getter class method for getting campaign list"""
    @classmethod
    def get_campaigns_list(cls):
        return cls.__campaigns
    
    """ Getter class method for adding to campaign list """
    @classmethod
    def __add_campaigns_list(cls,new_campaign):
        cls.__campaigns.append(new_campaign)

    """Setter method for changing active status of campaign"""
    def __set_status(self, status):
        self.is_active = status

    """Class method for turning status inactive for a brand id"""
    @classmethod
    def turn_off_campaigns_for_brand_id(cls, brand_id):
        for campaign in cls.get_campaigns_list():
            if campaign.get_brand_id() == brand_id:
                campaign.__set_status(False)

    """class method for turning status active for a brand id"""
    @classmethod
    def turn_on_campaigns_for_brand_id(cls, brand_id):
        for campaign in cls.get_campaigns_list():
            if campaign.get_brand_id() == brand_id:
                campaign.__set_status(True)


    """ Class method for adding new campaign obj """
    @classmethod
    def add_new_campaign(cls,campaign_id, campaign_brand_id, campaign_is_active, campaign_dayparting_hours):
        if campaign_id == None:
            campaign_id = len(cls.__campaigns)

        new_campaign = Campaign(id=campaign_id, brand_id=campaign_brand_id, is_active=campaign_is_active, dayparting_hours=campaign_dayparting_hours)
        cls.__add_campaigns_list(new_campaign)
        print("Campaign added successfully to Brand Id : ", campaign_brand_id, ". Campaign id : ", campaign_id)
    

    """Class method for getting all campaigns for a brand"""
    @classmethod
    def get_all_campaigns_for_brand_id(cls, brand_id):
        brand_campaigns = []
        for camp in cls.get_campaigns_list():
            if camp.get_id() == brand_id:
                brand_campaigns.append(camp)
        return brand_campaigns


    """Class method for reading all campaigns from a file"""
    @classmethod
    def read_campaigns_from_file(cls):
        try:
            file = open(cls.get_file_name(), 'r')
            for campaign in file.readlines():
                
                data = campaign.split(",")
                campaign_id = int(data[0])
                campaign_brand_id = int(data[1])
                campaign_is_active = bool(data[2])
                campaign_dayparting_hours = None if data[3] == 'None' else (data[3], data[4])
                cls.add_new_campaign(campaign_id, campaign_brand_id, campaign_is_active, campaign_dayparting_hours)
            print("Read all campaigns successfully from ", cls.get_file_name())
        except Exception as e:
            print("Error reading from campaigns file! Ensure file campaign.txt is present, and run program again.", e)
            os._exit(0)
        finally:
            file.close()

    """Class method for saving all campaigns to the file"""
    @classmethod
    def save_campaigns_to_file(cls):
        try:
            file = open(cls.get_file_name(), 'w')
            for campaign in cls.get_campaigns_list():
                to_write = str(campaign.get_id()) + "," +  \
                           str(campaign.get_brand_id()) + "," + \
                           str(campaign.get_active_status()) + ","
                if campaign.get_dayparting_schedule() == None:
                    to_write += str(campaign.get_dayparting_schedule()) + ",\n"
                else:
                    to_write += str(campaign.get_dayparting_schedule()[0]) + ',' + str(campaign.get_dayparting_schedule()[1]) + ',\n'
                file.write(to_write)
            print("Saved Campaigns successfully to ", cls.get_file_name())
        except:
            print("Error saving campaigns into the file! Ensure file campaign.txt is present, and run program again!")
            os._exit(0)
        finally:
            file.close()

    """Class method for displaying all campaigns on console"""
    @classmethod
    def display_all_campaigns(cls):
        print("\n\n")
        print("ID", "Brand Id", "Active Status", "Dayparting Hours", sep="   ")
        for campaign in cls.get_campaigns_list():
            print('{0:>2}'.format(campaign.get_id()), end='   ')
            print('{0:>8}'.format(campaign.get_brand_id()), end='   ')
            print('{0:>13}'.format(campaign.get_active_status()), end='   ')
            if campaign.get_dayparting_schedule():
                print('{0:>11}'.format(campaign.get_dayparting_schedule()[0]), end=' - ')
                print('{0:>2}'.format(campaign.get_dayparting_schedule()[1]))
            else:
                print('{0:>16}'.format(str(campaign.get_dayparting_schedule())))
        print("\n")
"""
Class Brands
    - it holds all the functions and class methods necessary for processing brand operation.
    - getter and setter methods for id, budgets and spendings
    - reading and saving all brands to file "brands.txt"
    - adding new brand and displaying all brands on screen
"""
class Brand:
    __brands = []
    __FILE_NAME = "brands.txt"
    __hour = 0

    def __init__(self, id, daily_budget, monthly_budget, daily_spend=0, monthly_spend=0, current_day=None):
        self.id = id
        self.budget_manager = BudgetManager(id, daily_budget, monthly_budget, daily_spend, monthly_spend, current_day)

    """Updating class variable to current time"""
    @classmethod
    def __set_hour(cls, hour):
        cls.__hour = hour
    
    """Getter method for hour"""
    @classmethod
    def __get_hour(cls):
        return cls.__hour

    """Getter method for retrieving brand id"""
    def get_id(self):
        return self.id
    
    """Getter method for retrieving brand id"""
    def get_daily_budget(self):
        return self.get_budget_manager().get_daily_budget()
    
    """Getter method for retrieving monthly budget"""
    def get_monthly_budget(self):
        return self.get_budget_manager().get_monthly_budget()
    
    """Getter method for retrieving daily spend"""
    def get_daily_spend(self):
        return self.get_budget_manager().get_daily_spend()
    
    """Getter method for retrieving monthly spend"""
    def get_monthly_spend(self):
        return self.get_budget_manager().get_monthly_spend()

    """Getter method for retrieving current day object"""
    def get_current_day(self):
        return self.get_budget_manager().get_current_day()

    """Getter method for retrieving current month"""
    def get_current_month(self):
        return self.get_budget_manager().get_current_month()

    """Getter method for retrieving budget manager for a brand"""
    def get_budget_manager(self):
        return self.budget_manager

    """Getter method for retrieving file name"""
    @classmethod
    def get_file_name(cls):
        return cls.__FILE_NAME
    
    """Getter class method for retrieving brands list"""
    @classmethod
    def get_brands_list(cls):
        return cls.__brands

    """Class method for adding brand to the brands list"""
    @classmethod
    def __add_brand_to_all_brands(cls, new_brand):
        cls.__brands.append(new_brand)        

    """Class method for reading brands from the file"""
    @classmethod
    def read_brands_from_file(cls):
        cls.__set_hour(datetime.datetime.now().hour)
        try:
            file = open(cls.get_file_name(), 'r')
            for brands in file.readlines():
                data = brands.split(",")
                cls.add_new_brand([int(data[0]), int(data[1]), int(data[2]), int(data[3]), int(data[4]), datetime.datetime.strptime(data[5],"%Y-%m-%d").date()])
            print("Read all brands successfully from ", cls.get_file_name())
        except Exception as e:
            print("Error reading from brands file! Ensure brands.txt file is present, and run program again.", e)
            os._exit(0)
        finally:
            file.close()
    
    """Class method for adding new brand"""
    @classmethod
    def add_new_brand(cls, brand_details):

        id = len(cls.__brands) if brand_details[0] == None else brand_details[0]
        daily_budget = brand_details[1]
        monthly_budget = brand_details[2]
        daily_spend = brand_details[3]
        monthly_spend = brand_details[4]
        current_day = brand_details[5]
        
        new_brand = Brand(id, daily_budget, monthly_budget, daily_spend, monthly_spend, current_day)
        cls.__add_brand_to_all_brands(new_brand)
        print("Brand added successfully! Brand id : ", id)


    """Class method for displaying all brand on screen"""
    @classmethod
    def display_all_brands(cls):
        print("\n\n")
        print("ID", "Daily Budget", "Monthly Budget", "Daily Spend", "Monthly Spend", sep="   ")
        for brand in cls.__brands:
            print('{0:>2}'.format(brand.get_id()), end='   ')
            print('{0:>12}'.format(brand.get_daily_budget()), end='   ')
            print('{0:>14}'.format(brand.get_monthly_budget()), end='   ')
            print('{0:>11}'.format(brand.get_daily_spend()), end='   ')
            print('{0:>13}'.format(brand.get_monthly_spend()))
        print("\n")
    """Class method for getting brand details for new brand from user"""
    @classmethod
    def get_new_brand_detail(cls):
        
        brand_details = [None]
        while True:
            try:
                daily_budget = int(input("Input daily budget: "))
                monthly_budget = int(input("Input monthly budget: "))
                if daily_budget < 0 or monthly_budget < 0:
                    raise ValueError
                break
            except ValueError:
                print("Enter Valid budget.(Only positive number)")                
        brand_details.append(daily_budget)
        brand_details.append(monthly_budget)
        brand_details.append(0)
        brand_details.append(0)
        brand_details.append(None)

        return brand_details

    """Class method for updating spending"""
    @classmethod
    def update_spending(cls):  
        while True:
            try:
                brand_id = int(input("Enter brand id: "))
                break
            except ValueError:
                print("Enter valid id(only numbers)")
        while not cls.if_id_exists(brand_id):
            try:
                brand_id = int(input("(id not found) Enter another brand id: "))
            except ValueError:
                print("Enter valid id(only numbers)")
        while True:
            try:
                spending_amout = int(input("Enter amount: "))
                break
            except ValueError:
                print("Enter valid amount(only numbers)")
        for brand in cls.get_brands_list():
            if brand.get_id() == brand_id:
                brand.get_budget_manager().check_and_update_spends(spending_amout)
                break
        print("\nSpending updated successfully\n")

    """Calss method to check if brand_id exist or not"""
    @classmethod
    def if_id_exists(cls, id):
        for brand in cls.get_brands_list():
            if brand.get_id() == id:
                return True
        return False
    
    """Enforcing dayparting scheduler"""
    @classmethod
    def enforce_dayparting_schedule(cls):
        if datetime.datetime.now().hour - cls.__get_hour() >= 1:
            cls.__set_hour(datetime.datetime.now().hour)
            for brand in cls.get_brands_list():
                brand.get_budget_manager().enforce_dayparting()

    
    """Class method to save all brands to the file"""
    @classmethod
    def save_brands_to_file(cls):
        try:
            file = open(cls.get_file_name(), 'w')
            for brand in cls.get_brands_list():
                to_write = str(brand.get_id()) + "," +  \
                           str(brand.get_daily_budget()) + "," + \
                           str(brand.get_monthly_budget()) + "," + \
                           str(brand.get_daily_spend()) + "," + \
                           str(brand.get_monthly_spend()) + "," + \
                           str(brand.get_current_day()) + "," + \
                           str(brand.get_current_month()) + "\n" 
                file.write(to_write)
            print("Saved brands successfully to ", cls.get_file_name())
        except Exception as e:
            print("Error saving brands into the file! Ensure file brands.txt is present, and run program again.", e)
            os._exit(0)
        finally:
            file.close()



"""
Class Budget Manager
    - handles budget for all brands
    - consist of getter and setter methods to retrieve and update all budget and spendings
    - methods to turn on and off campaigns
    - methods for evaluating budget and spendings
    - method for implementing dayparting schedule
"""
class BudgetManager:
    def __init__(self, brand_id, daily_budget, monthly_budget, daily_spend=0, monthly_spend=0, current_day = None):
        self.brand_id = brand_id
        self.daily_budget = daily_budget
        self.monthly_budget = monthly_budget
        self.daily_spend = daily_spend
        self.monthly_spend = monthly_spend
        if current_day:
            self.current_day = current_day
            self.current_month = self.current_day.month
        else:
            self.current_day = datetime.date.today()
            self.current_month = self.current_day.month
        self.reset_if_new_day()
        self.reset_if_new_month()

    """Getter method for retrieving brand id"""
    def get_brand_id(self):
        return self.brand_id
    
    """Getter method for retrieving daily budget"""
    def get_daily_budget(self):
        return self.daily_budget
    
    """Getter method for retrieving monthly budget"""
    def get_monthly_budget(self):
        return self.monthly_budget
    
    """Getter method for retrieving daily spend"""
    def get_daily_spend(self):
        return self.daily_spend
    

    """Getter method for retrieving monthly spend"""
    def get_monthly_spend(self):
        return self.monthly_spend
    
    """Getter method for retrieving current day"""
    def get_current_day(self):
        return self.current_day
    
    """Getter method for retrieving current month"""
    def get_current_month(self):
        return self.current_month
    
    """Setter method for updating daily spend"""
    def __set_daily_spend(self, spend_amount):
        self.daily_spend = spend_amount
    
    """Setter method for updating monthly spend"""
    def __set_monthly_spend(self, spend_amount):
        self.monthly_spend = spend_amount

    """Setter method for updating current day"""
    def __set_current_day(self, day):
        self.current_day = day
    
    """Setter method for updating current month"""
    def __set_current_month(self, month):
        self.current_month = month

    """Setter method for updating spending"""
    def check_and_update_spends(self, spend_amount):
        
        self.__set_daily_spend(self.get_daily_spend() + spend_amount)
        self.__set_monthly_spend(self.get_monthly_spend() + spend_amount)
        self.evaluate_budget_limits()

    """Method for checking spending limits with the budget"""
    def evaluate_budget_limits(self):
        if self.get_daily_spend() >= self.get_daily_budget():
            self._turn_off_campaigns(reason="Daily budget hit")
        if self.get_monthly_spend() >= self.get_monthly_budget():
            self._turn_off_campaigns(reason="Monthly budget hit")

    """Method for turning campaigns off"""
    def _turn_off_campaigns(self, reason=""):
        Campaign.turn_off_campaigns_for_brand_id(self.get_brand_id())
        print(f"Turned off campaigns for Brand {self.get_brand_id()} - Reason: {reason}")

    """Method for turning campaigns on"""
    def _turn_on_campaigns(self):
        Campaign.turn_on_campaigns_for_brand_id(self.get_brand_id())
        print(f"Turned on campaigns for Brand {self.get_brand_id()}")

    """Resetting spendings if the new day starts"""
    def reset_if_new_day(self):
        today = datetime.date.today()
        if today != self.get_current_day():
            print("Resetting daily spends...")
            
            self.__set_daily_spend(0)
            if self.get_monthly_spend() < self.get_monthly_budget():
                self._turn_on_campaigns()
            self.__set_current_day(today)
    """Resetting spendings if the new month starts"""
    def reset_if_new_month(self):
        today = datetime.date.today()
        if today.month != self.get_current_month():
            print("Resetting monthly spends...")
            self.__set_monthly_spend(0)
            self.__set_daily_spend(0)
            self._turn_on_campaigns()
            self.__set_current_month(today.month)

    """Method for controlling campaigns with hourly schedule"""
    def enforce_dayparting(self):
        current_hour = datetime.datetime.now().hour
        
        for campaign in Campaign.get_all_campaigns_for_brand_id(self.get_brand_id()):
            if campaign.get_dayparting_schedule():
                start, end = campaign.get_dayparting_schedule()
                if start <= current_hour < end:
                    if self.get_daily_spend() < self.get_daily_budget() and self.get_monthly_spend() < self.get_monthly_budget():
                        campaign.set_active_status(True)
                else:
                    campaign.set_active_status(False)

"""
Class Main
    - consists of all functions related to user interface
    - Built to abstract the backend from frontend
    - Holds the starting point of all functions

"""
class Main():
    menu_list = ["1. Add new brand",
                 "2. Add campaign to existing brand",
                 "3. List all brands with details",
                 "4. Update Spending.",
                 "5. List all campaign with details",
                 "6. Exit"]
    def __init__(self):
        Campaign.read_campaigns_from_file()
        Brand.read_brands_from_file()

    def show_main_menu(self):
        print("\n\nSelect option: ")
        for option in self.menu_list:
            print(option)

    def get_user_input(self):
        while True:
            try:
                option = int(input("Select option: "))
                break
            except ValueError:
                print("Enter valid option.(number only)")
        return option
    
    def get_new_campaign_details(self):
        campaign_details = []
        while True:
            try:
                id = int(input("Enter brand id: "))
                while not Brand.if_id_exists(id):
                    id = int(input("(id not found) Enter another brand id: "))
                campaign_details.append(id)
                campaign_details.append(True) 
                dayparting_choice = input("Do you want dayparting hours:").lower()
                if dayparting_choice in ['y', 'n']:
                    if dayparting_choice == 'y':
                        h1 = int(input("Enter start hour[0-24]: "))
                        h2 = int(input("Enter end hour[0-24]: "))
                        if h1 > h2:
                            print("Star hour should be less than end hour.")
                            raise ValueError
                        campaign_details.append((h1,h2))
                    else:
                        campaign_details.append(None)   
                               
                    break
                else:
                    print("Enter valid choice (y/n)")
            except ValueError:
                print("Enter valid number.")
        return campaign_details
    
    def save_everything(self):
        Brand.save_brands_to_file()
        Campaign.save_campaigns_to_file()
    
    def perform_loop(self):
        while True:
            self.show_main_menu()
            option = self.get_user_input()
            self.perform_task(option)
            Brand.enforce_dayparting_schedule()

    def perform_task(self, option):

        if option == 1:
            Brand.add_new_brand(Brand.get_new_brand_detail())
        elif option == 2:
            campaign_brand_id, campaign_is_active, campaign_dayparting_hours = self.get_new_campaign_details()
            Campaign.add_new_campaign(None, campaign_brand_id, campaign_is_active, campaign_dayparting_hours)
        elif option == 3:
            Brand.display_all_brands()
        elif option == 4:
            Brand.update_spending()

        elif option == 5:
            Campaign.display_all_campaigns()
        elif option == 6:
            self.save_everything()
            os._exit(0)
        else:
            print("Options available from 1-5. Try again.")


program = Main()
program.perform_loop()
