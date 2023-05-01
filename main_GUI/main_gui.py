'''
Name : Python Bytes
Team Members : Kayla (kmcfarla) , David (dsanche2), Ruth (rpeter)
'''


'''
Function : main_gui.py 
Main function to run the GUI screen

'''

import tkinter as tk
from tkinter import messagebox
import threading
import pandas as pd
from tkinter import ttk
from web_scraping import scrapeHolidify
from flight_function import flight_info


'''
Function called when the search button is clicked 
:param :
:return:
'''
def search_button_click():
    try:
        ## fetch values from the entry boxes
        source = source_entry.get().lower()
        dest = dest_entry.get().lower()
        arrival = arrival_entry.get().lower()
        departure = departure_entry.get().lower()
    except ValueError:
        messagebox.showerror("Error", "Invalid input")
        return

    # Start 3 threads to fetch the data
    t1 = threading.Thread(target=fetch_attraction_places, args=(dest,))
    t1.start()
    t2 = threading.Thread(target=fetch_web_scraping, args=(dest,))
    t2.start()
    t3 = threading.Thread(target=fetch_flight_information, args = (source, dest, arrival, departure , ))
    t3.start()


'''
Function : fetch_flight_information
This function fetches flight information based on the source, destination, arrival and departure parameters
: param : source, dest, arrival, departure
: return : 
'''
def fetch_flight_information(source, dest, arrival, departure):

    # Get the flight information for the provided parameters
    flight_list = flight_info(source, dest, arrival, departure)

    # listbox to display the flight information
    flight_listbox = tk.Listbox(root, height=10, width=100)
    flight_listbox.grid(row=7, column=1,columnspan=2)

    if len(flight_list) == 0 :
        flight_listbox.insert(tk.END, 'No Flights Found')
    else:
        # Loop through the list of flights and extract the itinerary information
        for flights in flight_list:
            itinerary1 = flights['itinerary1']
            itinerary2 = flights['itinerary2']

            departure_string = "Duration of the first flight: %s. The departure is from: \
                %s. The departure time is: %s. You will arrive in the airport with IATA code: %s\
                     at %s time."%(itinerary1['duration'], itinerary1['departure'],
                                             itinerary1['departure_time'], itinerary1['arrival'],
                                             itinerary1['arrival_time'])

            return_string = "Duration of the second flight: %s. The departure is from: \
                %s. The departure time is: %s. You will arrive in the airport with IATA code: %s \
                    at %s time."%(itinerary2['duration'], itinerary2['departure'],
                                             itinerary2['departure_time'], itinerary2['arrival'],
                                             itinerary2['arrival_time'])

            # insert values in the listbox
            flight_listbox.insert(tk.END, departure_string + '\n' + return_string)


'''
Function : fetch_flight_information
This function fetches hotel information by web scraping from Holidify website.
: param : source, dest, arrival, departure
: return : 
'''
def fetch_web_scraping(dest):

    #call the method to fetch the hotel list
    hotel_list = scrapeHolidify(dest.lower())

    # listbox to display the flight hotel information
    hotel_listbox = tk.Listbox(root, height=10, width=100)
    hotel_listbox.grid(row=9, column=1,columnspan=2)

    # Loop through hotel and insert its name and price in the hotel list box.
    for hotel in hotel_list:
        name, price = hotel
        hotel_listbox.insert(tk.END, name + "---- Total Price :"+price)


'''
Function which returns a list of attractions with details based on the destination provided
:param dest:
:return:
'''
def fetch_attraction_places(dest):

    df = pd.read_csv('data/tourist_attractions.csv')


    # filter on attraction and state
    attraction_filter = df['attraction'].str.contains(dest, case=False)
    state_filter = df['state'].str.contains(dest, case=False)

    # if attraction name found, fetch all the attractions in the state
    if attraction_filter.any():
        test_df = df[attraction_filter]
        state = test_df['state'].iloc[0]
        print(state)
        filtered_df = df[df['state'] == state]
    else:
        filtered_df = df[state_filter]

    result_text = ""

    # loop through the df, fetch values
    for index, row in filtered_df.iterrows():
        attraction = row['attraction']
        ideal_duration = row["ideal_duration"]
        best_time = row["best_time"]
        description = row["description"]

        # Append the values to the result label
        result_text += "attraction: " + attraction + "\n" + "Ideal duration: " + str(
            ideal_duration) + "\n" + "Best time to visit: " + str(best_time) + "\n" \
                       + "Description: " + str(description) + "-------------------------------------\n"

        result_label.configure(state="normal")
        result_label.delete("1.0", tk.END)  # clear the existing content
        result_label.insert(tk.END, result_text)  # insert the new content
        result_label.configure(state="disabled")

    scrollbar.config(command=result_label.yview)


# create main GUI window
root = tk.Tk()
root.geometry("700x1000")
root.title("Travel Planner")

# create label headers
header_label = ttk.Label(root, text="My Travel Planner", font=("Arial", 24, "bold"), anchor="center")
header_label.grid(row=0, column=0, columnspan=3, sticky='nsew',pady=5)
header_label.configure(anchor='center')


# Create labels and entry fields for the user to input search parameters
input_label = tk.Label(root, text="Enter source destination")
input_label.grid(row=1, column=1, sticky='w')
input_label.configure(anchor='center')

source_entry = tk.Entry(root)
source_entry.grid(row=1, column=2)

input_label_2 = tk.Label(root, text="Enter travel destination")
input_label_2.grid(row=2, column=1, sticky='w')
input_label_2.configure(anchor='center')

dest_entry = tk.Entry(root)
dest_entry.grid(row=2, column=2)

input_label_3 = tk.Label(root, text="Enter Departure Date")
input_label_3.grid(row=3, column=1, sticky='w')
input_label_3.configure(anchor='center')

departure_entry = tk.Entry(root)
departure_entry.grid(row=3, column=2)

input_label_4 = tk.Label(root, text="Enter arrival Date")
input_label_4.grid(row=4, column=1, sticky='w')
input_label_4.configure(anchor='center')

arrival_entry = tk.Entry(root)
arrival_entry.grid(row=4, column=2)

search_button = tk.Button(root, text="Search", command=search_button_click)
search_button.grid(row=5, column=2, sticky="nw")


# create label headers
header_label_2 = ttk.Label(root, text="Flight Details ", font=("Arial", 18, "bold"), anchor="center")
header_label_2.grid(row=6, column=0, columnspan=3, sticky='nsew')
header_label_2.configure(anchor='center')

header_label_3 = ttk.Label(root, text="Hotel Details ", font=("Arial", 18, "bold"), anchor="center")
header_label_3.grid(row=8, column=0, columnspan=3, sticky='nsew')
header_label_3.configure(anchor='center')


header_label_4 = ttk.Label(root, text="Attraction Details ", font=("Arial", 18, "bold"), anchor="center")
header_label_4.grid(row=10, column=0, columnspan=3, sticky='nsew')
header_label_4.configure(anchor='center')


# Create a frame to hold the result_label and scrollbar
result_frame = ttk.Frame(root)
result_frame.grid(row=  11, column=1, columnspan=2, sticky="nsew")
root.rowconfigure(5, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)
result_frame.rowconfigure(0, weight=1)
result_frame.columnconfigure(0, weight=1)

# Create the result_label and scrollbar
result_label = tk.Text(result_frame, wrap="word")
result_label.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=result_label.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Attach the scrollbar to the result_label
result_label.configure(yscrollcommand=scrollbar.set)

image_label = tk.Label(root, image="")
image_label.grid(row=5, column=2)
root.mainloop()
