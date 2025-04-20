import datetime
import os

class Campaign:
    __campaigns = []
    def __init__(self, id, brand_id, is_active=True, dayparting_hours=(-1,-1)):
        self.id = id
        self.brand_id = brand_id
        self.is_active = is_active
        self.dayparting_hours = dayparting_hours  # Tuple like (start_hour, end_hour)
    
    @classmethod
    def __add_campaigns(cls,campaign_id, campaign_brand_id, campaign_is_active, campaign_dayparting_hours):
        if campaign_dayparting_hours == (-1, -1):
            campaign_dayparting_hours = None
        new_campaign = Campaign(id=campaign_id, brand_id=campaign_brand_id, is_active=campaign_is_active, dayparting_hours=campaign_dayparting_hours)
        cls.__campaigns.append(new_campaign)
    
    @classmethod
    def get_all_campaigns_for_brand_id(cls, brand_id):
        brand_campaigns = []
        for camp in cls.__campaigns:
            if camp.id == brand_id:
                brand_campaigns.append(camp)
        return brand_campaigns

    @classmethod
    def read_campaigns_from_file(cls):
        FILE_NAME = "campaigns.txt"
        try:
            file = open(FILE_NAME, 'r')
            for campaign in file.readlines():
                data = campaign.split(",")
                campaign_id = int(data[0])
                campaign_brand_id = int(data[1])
                campaign_is_active = bool(data[2])
                campaign_dayparting_hours = (int(data[3]), int(data[4]))
                cls.__add_campaigns(campaign_id, campaign_brand_id, campaign_is_active, campaign_dayparting_hours)
        finally:
            file.close()
        
    @classmethod
    def add_new_campaign(cls, campaign_details):
        id = len(cls.__campaigns)
        brand_id = campaign_details[0]
        new_campaign = Campaign(id, brand_id, dayparting_hours=campaign_details[1])
        cls.__campaigns.append(new_campaign)

    @classmethod
    def save_campaigns_to_file(cls):
        FILE_NAME="campaign.txt"
        try:
            file = open(FILE_NAME, 'w')
            for campaign in cls.__campaigns:
                to_write = str(campaign.id) + "," +  \
                           str(campaign.brand_id) + "," + \
                           str(campaign.is_active) + "," + \
                           str(campaign.dayparting_hours) + "\n"
                file.write(to_write)
        finally:
            file.close()

    @classmethod
    def display_all_campaigns(cls):
        print("ID", "Brand Id", "Active Status", "Dayparting Hours", sep="   ")
        for campaign in cls.__campaigns:
            print('{0:>2}'.format(campaign.id), end='   ')
            print('{0:>8}'.format(campaign.brand_id), end='   ')
            print('{0:>13}'.format(campaign.is_active), end='   ')
            print('{0:>11}'.format(campaign.dayparting_hours[0]), end=' - ')
            print('{0:>2}'.format(campaign.dayparting_hours[1]))

        

class Brand:
    __brands = []

    def __init__(self, id, daily_budget, monthly_budget, daily_spend=0, monthly_spend=0, campaigns = [], current_day=None):
        self.id = id
        self.budget_manager = BudgetManager(id, daily_budget, monthly_budget, daily_spend, monthly_spend, campaigns, current_day)



    @classmethod
    def add_brand_to_all_brands(cls, new_brand):
        cls.__brands.append(new_brand)        

    @classmethod
    def read_brands_from_file(cls):
        FILE_NAME = "brands.txt"
        try:
            file = open(FILE_NAME, 'r')
            for brands in file.readlines():
                data = brands.split(",")
                brand_id = int(data[0])
                brand_daily_budget = int(data[1])
                brand_monthly_budget = int(data[2])
                brand_daily_spend = int(data[3])
                brand_monthly_spend = int(data[4])
                brand_current_day = int(data[5])
                brand_campaigns = Campaign.get_all_campaigns_for_brand_id(brand_id=brand_id)
                new_brand = Brand(brand_id, brand_daily_budget, brand_monthly_budget, brand_daily_spend, brand_monthly_spend, brand_campaigns, brand_current_day)
                cls.add_brand_to_all_brands(new_brand)
        finally:
            file.close()
    
    @classmethod
    def add_new_brand(cls, brand_details):
        daily_budget, monthly_budget = brand_details[0], brand_details[1] 
        id = len(cls.__brands)
        new_brand = Brand(id, daily_budget, monthly_budget)
        cls.add_brand_to_all_brands(new_brand)

    @classmethod
    def display_all_brands(cls):
        print("ID", "Daily Budget", "Monthly Budget", "Daily Spend", "Monthly Spend", sep="   ")
        for brand in cls.__brands:
            print('{0:>2}'.format(brand.id), end='   ')
            print('{0:>12}'.format(brand.budget_manager.daily_budget), end='   ')
            print('{0:>14}'.format(brand.budget_manager.monthly_budget), end='   ')
            print('{0:>11}'.format(brand.budget_manager.daily_spend), end='   ')
            print('{0:>13}'.format(brand.budget_manager.monthly_spend))



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
        for brand in cls.__brands:
            if brand.id == brand_id:
                brand.budget_manager.check_and_update_spends(spending_amout)
                break

    @classmethod
    def if_id_exists(cls, id):
        for brand in cls.__brands:
            if brand.id == id:
                return True
        return False
    
    @classmethod
    def save_brands_to_file(cls):
        FILE_NAME="brands.txt"
        try:
            file = open(FILE_NAME, 'w')
            for brand in cls.__brands:
                to_write = str(brand.id) + "," +  \
                           str(brand.budget_manager.daily_budget) + "," + \
                           str(brand.budget_manager.monthly_budget) + "," + \
                           str(brand.budget_manager.daily_spend) + "," + \
                           str(brand.budget_manager.monthly_spend) + "," + \
                           str(brand.budget_manager.current_day) + "," + \
                           str(brand.budget_manager.current_month) + "\n" 
                file.write(to_write)
        finally:
            file.close()




class BudgetManager:
    def __init__(self, brand_id, daily_budget, monthly_budget, daily_spend=0, monthly_spend=0, campaigns = [], current_day = None):
        self.brand_id = brand_id
        self.daily_budget = daily_budget
        self.monthly_budget = monthly_budget
        self.daily_spend = daily_spend
        self.monthly_spend = monthly_spend
        self.campaigns = campaigns
        if current_day:
            self.current_day = current_day
            self.current_month = self.current_day.month
        else:
            self.current_day = datetime.date.today()
            self.current_month = self.current_day.month
        self.reset_if_new_day()
        self.reset_if_new_month()

    def check_and_update_spends(self, spend_amount):
        
        self.daily_spend += spend_amount
        self.monthly_spend += spend_amount
        self.evaluate_budget_limits()

    def evaluate_budget_limits(self):
        if self.daily_spend >= self.daily_budget:
            self._turn_off_campaigns(reason="Daily budget hit")
        if self.monthly_spend >= self.monthly_budget:
            self._turn_off_campaigns(reason="Monthly budget hit")

    def _turn_off_campaigns(self, reason=""):
        for campaign in self.campaigns:
            campaign.is_active = False
        print(f"Turned off campaigns for Brand {self.brand_id} - Reason: {reason}")

    def _turn_on_campaigns(self):
        for campaign in self.campaigns:
            campaign.is_active = True

    def reset_if_new_day(self):
        today = datetime.date.today()
        if today != self.current_day:
            print("Resetting daily spends...")
            
            self.daily_spend = 0
            if self.monthly_spend < self.monthly_budget:
                self._turn_on_campaigns()
            self.current_day = today

    def reset_if_new_month(self):
        today = datetime.date.today()
        if today.month != self.current_month:
            print("Resetting monthly spends...")
            self.monthly_spend = 0
            self.daily_spend = 0
            self._turn_on_campaigns()
            self.current_month = today.month

    def enforce_dayparting(self):
        current_hour = datetime.datetime.now().hour
        
        for campaign in self.campaigns:
            if campaign.dayparting_hours:
                start, end = campaign.dayparting_hours
                if start <= current_hour < end:
                    if self.daily_spend < self.daily_budget and self.monthly_spend < self.monthly_budget:
                        campaign.is_active = True
                else:
                    campaign.is_active = False

class Main():
    def __init__(self):
        Campaign.read_campaigns_from_file()
        Brand.read_brands_from_file()

    def show_main_menu(self):
        print("Select option: ")
        print("1. Add new brand")
        print("2. Add campaign to existing brand")
        print("3. List all brands with details")
        print("4. Update Spending.")
        print("5. List all campaign with details")
        print("6. Exit")

    def get_user_input(self):
        while True:
            try:
                option = int(input("Select option: "))
                break
            except ValueError:
                print("Enter valid option.(number only)")
        return option
    
    def get_new_brand_detail(self):
        brand_details = []
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
        return brand_details
    
    def get_new_campaign_details(self):
        campaign_details = []
        while True:
            try:
                id = int(input("Enter brand id: "))
                while not Brand.if_id_exists(id):
                    id = int(input("(id not found) Enter another brand id: "))
                campaign_details.append(id)
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
                        campaign_details.append((-1,-1))               
                    break
                else:
                    print("Enter valid choice (y/n)")
                
            except ValueError:
                print("Enter valid number.")
        
        return campaign_details
    
    def save_everything(self):
        Brand.save_brands_to_file()
        Campaign.save_campaigns_to_file()
    
    def perform_task(self):
        while True:
            self.show_main_menu()
            option = self.get_user_input()
            if option == 1:
                brand_details = self.get_new_brand_detail()
                Brand.add_new_brand(brand_details)
            elif option == 2:
                campaign_details = self.get_new_campaign_details()
                Campaign.add_new_campaign(campaign_details)
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


def run_program():
    program = Main()
    program.perform_task()

run_program()
