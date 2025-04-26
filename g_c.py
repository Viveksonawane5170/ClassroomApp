from phi.agent import Agent
from phi.tools.googlecalendar import GoogleCalendarTools
import datetime
from phi.model.google import Gemini
from tzlocal import get_localzone_name
import os

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def get_valid_datetime_input():
    """Get valid date and time input from user"""
    while True:
        try:
            date_str = input("Enter date (DD-MM-YYYY): ")
            day, month, year = map(int, date_str.split('-'))
            input_date = datetime.date(year, month, day)
            
            time_str = input("Enter time in 24-hour format (HH:MM): ")
            hour, minute = map(int, time_str.split(':'))
            if not (0 <= hour <= 23 and 0 <= minute <= 59):
                raise ValueError("Invalid time")
                
            return input_date, f"{hour:02d}:{minute:02d}"
        except ValueError as e:
            print(f"Invalid input: {e}. Please try again.")

# Initialize the agent
agent = Agent(
    tools=[GoogleCalendarTools(credentials_path="./credentials.json")],
    model=Gemini(id="gemini-2.0-flash-exp", temperature=0.4),
    show_tool_calls=True,
    instructions=[
        f"""
        You are scheduling assistant. Today is {datetime.datetime.now()} and the users timezone is {get_localzone_name()}.
        You should help users to perform these actions in their Google calendar:
            - get their scheduled events from a certain date and time
            - create events based on provided details
        """
    ],
    add_datetime_to_instructions=True,
)

# Get user input
print("Let's create a 'Hello' event in your Google Calendar")
event_date, event_time = get_valid_datetime_input()
timezone = get_localzone_name()

# Format date for Google Calendar (YYYY-MM-DD)
formatted_date = event_date.strftime("%Y-%m-%d")

# Create the event
agent.print_response(
    f"Create an event in my calendar titled 'Ram Ram' on {formatted_date} at {event_time} {timezone} that lasts 30 minutes", 
    
    markdown=True
)

print(f"\nEvent 'Hello' scheduled for {event_date.strftime('%d-%m-%Y')} at {event_time} {timezone}")