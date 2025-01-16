import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#load work_times.csv into a DataFrame
work_df = pd.read_csv('work_times.csv')


work_df['date'] = pd.to_datetime(work_df['date'])  # Converted the date into datetime
#converted start_time and end_time into datetime and military (24 h) format so I could work with the time easier
work_df['start_time'] = pd.to_datetime(work_df['start_time'], format='%H:%M')
work_df['end_time'] = pd.to_datetime(work_df['end_time'], format='%H:%M')


#I've putted the date and the start_time and end_time columns to make timestamps
#extracted hours and minutes from the time columns, converted them to timedelta objects, so I could get precise start and end timestamps
work_df['start_datetime'] = work_df['date'] + pd.to_timedelta(work_df['start_time'].dt.hour, unit='h') \
                                        + pd.to_timedelta(work_df['start_time'].dt.minute, unit='m')

work_df['end_datetime'] = work_df['date'] + pd.to_timedelta(work_df['end_time'].dt.hour, unit='h') \
                                        + pd.to_timedelta(work_df['end_time'].dt.minute, unit='m')

#calculated gross and work hours
work_df['gross_hours'] = (work_df['end_datetime'] - work_df['start_datetime']).dt.total_seconds() / 3600 #calculated gross time (not including breaks) by subsctructing end and start time to get this in hours 
work_df['work_hours'] = work_df['gross_hours'] - (work_df['break_minutes'] / 60) #calculated total work time by subsctucting gross time and break (since I'm using gross time in hours, I've converted break time into hours)
#extracted the numeric part out of the employee_id  by filtering out numbers, joining them into a string and converting into the number

print("Processed data:")
print(work_df.head())
#extracted the numbers part of the employee_id via lambda function.
work_df['emp_number'] = work_df['employee_id'].apply(lambda x: int(''.join(filter(str.isdigit, x))))

print("\nUnique Employee ID Parsing:")
print(work_df[['employee_id', 'emp_number']].head())

#loaded csv file into a DF and set the employee_id column as the index
employees_info = pd.read_csv('employees_info.csv').set_index('employee_id')
work_df = work_df.set_index('employee_id').join(employees_info, how='inner').reset_index()

print("\nData after joining with employee information:")
print(work_df.head())

#defined a function to calculate total working hours and avg daily work hours
def employee_summary(employee_id):
    """Provided a concise summary of work data for a specific employee."""
    emp_data = work_df[work_df['employee_id'] == employee_id]
    total_days = emp_data['date'].nunique()
    total_hours = emp_data['work_hours'].sum()
    avg_hours = total_hours / total_days if total_days else 0
    return {
        "Days Worked": total_days,
        "Total Hours": total_hours,
        "Average Hours": avg_hours
    }

print("\nEmployee Summary for E001:")
print(employee_summary('E001')) #Define an employee by changing ID

#defined a function to find the best performed days for a specific worker

def longest_days(employee_id, top_n=3):
    #ffound the top N days with the highest working hours for the specified employee
    emp_data = work_df[work_df['employee_id'] == employee_id].copy()
    emp_data.sort_values('work_hours', ascending=False, inplace=True)
    return emp_data.head(top_n)[['date', 'work_hours']]

print("\nLongest working days for E001:")
print(longest_days('E001'))

#filtered supervisors who worked overtime (their working time is > 8)
supervisor_condition = (work_df['role'] == 'Supervisor') & (work_df['work_hours'] > 8)
supervisor_overtime = work_df[supervisor_condition]

print("\nSupervisors who worked overtime:")
print(supervisor_overtime)

#find employees who took breaks shorter than 30 minutes

office_less_break = work_df.query("store_location == 'Office' and break_minutes < 30")

print("\nOffice employees with short breaks:")
print(office_less_break)


work_df['week_number'] = work_df['date'].dt.isocalendar().week

#created a pivot table to define total weekly work hours for each employee
weekly_pivot = work_df.pivot_table(values='work_hours', index='employee_id', columns='week_number', aggfunc='sum', fill_value=0)

#found the employee who worked the most hours for each week 
max_hours_per_week = weekly_pivot.idxmax()

print("\nWeekly pivot table (total hours per employee):")
print(weekly_pivot)

print("\nEmployee with maximum hours each week:")
print(max_hours_per_week)

#calculated the average daily work hours for each employee 
avg_hours = work_df.groupby('employee_id')['work_hours'].mean()

# Built a graph of an the average daily work hours using a bar plot (x for IDs, y for avg hours)
sns.barplot(x=avg_hours.index, y=avg_hours.values, palette="Blues_d")
plt.title('Average Daily Hours per Employee')
plt.xlabel('Employee ID')
plt.ylabel('Average Daily Hours')
plt.show()

#filtered data for a specific employee (x for week numbers, y for hours)
emp_weekly = work_df[work_df['employee_id'] == chosen_emp].groupby('week_number')['work_hours'].sum()

emp_weekly.plot(kind='bar', color='black', legend=False)
plt.title(f'Total Weekly Hours for {chosen_emp}')
plt.xlabel('Week Number')
plt.ylabel('Total Hours')
plt.grid(True)
plt.show()


work_df['weekday'] = work_df['date'].dt.day_name()

#found the avg daily hours 
weekday_avg = work_df.groupby(['employee_id', 'weekday'])['work_hours'].mean().reset_index()
weekday_avg['weekday'] = pd.Categorical(weekday_avg['weekday'], 
                                        categories=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], 
                                        ordered=True)
weekday_avg.sort_values(['employee_id', 'weekday'], inplace=True)

#defined the weekday on which each employee worked the most hours by finding the row with the maximum work_hours for each employee.
most_active_weekday = weekday_avg.loc[weekday_avg.groupby('employee_id')['work_hours'].idxmax()]

print("\nAverage daily hours by weekday:")
print(weekday_avg)

print("\nMost active weekday for each employee:")
print(most_active_weekday)
#TASK 1
import random

#function to start and manage the game
def start_rock_paper_scissors():
#possible choices
    choices = {'r': 'Rock', 'p': 'Paper', 's': 'Scissors'}
   #defining the input
    user_input = input("Enter your choice (r for Rock, p for Paper, s for Scissors): ").lower()

    if user_input not in choices:
    	#gonna check if the input is right
        print("Invalid input! Please select either 'r' for Rock, 'p' for Paper, or 's' for Scissors.")
        return  # End the game if invalid input is provided
    

    print(f"You chose: {choices[user_input]}")
    #in this case we are asking computer to do the choice randomly
    computer_choice = random.choice(list(choices.keys()))
    print(f"Computer chose: {choices[computer_choice]}")

    if user_input == computer_choice:
    	#a tie
        print("It's a tie! Both chose the same.")
    elif (user_input == 'r' and computer_choice == 's') or (user_input == 'p' and computer_choice == 'r') or (user_input == 's' and computer_choice == 'p'):
        #sser wins 
        print("You win! Congratulations!")
    else:
    	#user loses
        print("Computer wins! Better luck next time.")


    play_again = input("Do you want to play again? (y/n): ").lower()
    
    if play_again == 'y':

        start_rock_paper_scissors()
    else:
        #if the user chooses 'n', thank them for playing and end the game
        print("Thank you for playing! Goodbye.")


start_rock_paper_scissors()

#TASK 2

def kelvin_to_human(kelvin_temp):
	@the temperature grade

    if kelvin_temp <= 274:
        return "Freezing"
    elif kelvin_temp <= 284:
        return "Cold"
    elif kelvin_temp <= 294:
        return "Cool"
    elif kelvin_temp <= 304:
        return "Warm"
    else:
        return "Hot"

#testing the function with different Kelvin values
test_temps = [500, 10, 300]

for temp in test_temps:
    human_readable = kelvin_to_human(temp)
    print(f"The temperature {temp} K is considered '{human_readable}'.")
