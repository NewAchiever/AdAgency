# AdAgency

The code here manages the budget and spending of brands for an ad agency.

# Table of Content


1. Pseudocode
2. How to run the code



# 1. Pseudocode
The pseudocode here will give the general overview of design and execution of the project.

The project has four classes:
  
- Campaigns
- Brands
- BudgetManager
- Main

#### Class Campaigns

Each campaign object has its **id**, **brand_id**, **active_status**, **dayparting_schedule**
This object is accessed by BudgetManager to ON/OFF  active_status and enforce dayparting schedule. 

    init():
        id
        brand_id
        is_active
        dayparting_hours
    
    turn_on_campaigns_for_brand_id(brand_id)
        for campaign in campaigns_list:
            if campaign.brand_id == brand_id:
                campaign.is_active = True
    
    turn_off_campaigns_for_brand_id(brand_id)
        for campaign in campaigns_list:
            if campaign.brand_id == brand_id:
                campaign.is_active = False


#### Class Brands:
Class brands, has its **id** and a **budget manager** for each object.
**Budget manager** handles all the functionality for managing spendings, budget, dayparting schedule and turning campaigns on/off. 

Brand class also has a **enforce_dayparting_schedule** method, which allows to check dayparting schedule every hour, and check all campaigns of each brand, and turn on/off if required.

This method is run in infinite loop in the **perform_loop** method of the **Main class**, but each campaign is checked only once per hour.

    init()
        brand_id
        budget_manager = BudgetManager()
    
    def update_spending(cls):  
        while True:
            try:
                brand_id = input("Enter brand id: ")
                break
            except ValueError:
                print("Enter valid id")
        while not cls.if_id_exists(brand_id):
            try:
                brand_id = input("(id not found) Enter another brand id: ")
            except ValueError:
                print("Enter valid id")
        while True:
            try:
                spending_amout = input("Enter amount: ")
                break
            except ValueError:
                print("Enter valid amount")
        for brand in get_brands_list():
            if brand.id == brand_id:
                check_and_update_spends(spending_amout)


    def enforce_dayparting_schedule():
        if datetime.datetime.now().hour - saved_hour >= 1:
            saved_hour = datetime.datetime.now().hour
            for brand in brand_list:
                brand.get_budget_manager().enforce_dayparting()
                

#### Class BudgetManager:
When a **Brand** object is created, a BudgetManager object is assigned to it. Hence, Budget Manager handles each brand seperately.

    def check_and_update_spends(spend_amount):
        update_daily_spending()
        update_monthly_spending()
        evaluate_budget_limits()


    def evaluate_budget_limits():
        if daily_spend >= daily_budget:
            turn_off_campaign_for_brand_id
        if monthly_spend >= monthly_budget:
            turn_of_campaign_for_brand_id
    
    def reset_if_new_day():
        if datetime.today() != self.current_day  #if it is new day 
            set_daily_spend = 0
            if monthly_spend < monthly_budget:
                turn_on_campaign_for_brand_id
            self.current_day = datetime.today()
    
    def reset_if_new_month():
        if datetime.today().month != self.current_month # if it is new month
            set_daily_spend = 0
            set_monthly_spend = 0
            turn_on_campaign_for_brand_id
            self.current_month = datetime.today().month

    def enforce_dayparting():
        current_hour = today.hour
        for campaign in list_of_campaign_for_brand_id:
            if campaign.is_dayparting_allowed:
                start, end = campaign.get_dayparting_schedule()
                if start <= current_hour and current_hour < end:
                    if daily_spend < daily_budget and monthly_spend < monthly_budget:
                        campaign.set_active_status(True) # Turn on campaign
                    else:
                        campaign.set_active_status(False) # Turn off campaign

#### Class Main
Main class defined user experience. It abstracts the backend system from the front-end. 

    def init():
        read_all_campaigns_from_file()
        read_all_brands_from_file()
    
    def perform_loop():
        show_menu()
        option = take_user_input()
        perform_task(option)
    
    def perform_task(option):
        if option == 1:
            add_brand()
        elif optioin == 2:
            add_campaign()
        elif option == 3:
            display_all_brands()
        elif option == 4:
            update_spending()
        elif option == 5:
            display_campaigns()
        elif option == 6:
            save_everything()
            exit()





# 2. How to run the code

**NOTE:** To run the code, make sure **brands.txt** and **campaigns.txt** are in the same directory of **AdAgency.py**

Steps:
1. Download the source code into the folder. 
2. Open the any terminal of your choice: VSCode or CMD.
3. Inside the terminal write:
    **cd path/to/directory_where_project_files_is_saved/** 
4. Write the command: 
   1. py **AdAgency.py** OR
   2. python **AdAgency.py** OR
   3. python3 **AdAgency.py**
5. The program will display a menu of available function to test the program. It will have following menu in the same order:
   
   1. Add new brand
   2. Add campaign
   3. List all brands
   4. Update spending
   5. List all campaigns
   6. Exit
   
6. You can see the existing brands and campaigns saved in the file by selecting **5** and **3** options.
7. Selecting for **Adding new brand** will prompt for
   - Daily budget
   - Monthly budget.
8.  **Adding campaign** will ask for 
     - Brand id for which campaign is being added
     - Are you interested in dayparting schedule.
       - If **y**, then it will ask for start and end hours
9.  **Update spending** will prompt user for amount of spending. It will evaluate the spending against the budget.
10. **Exit** will save everything to file and close the program.
     
