import tkinter as tk
from io import BytesIO
from tkinter import messagebox
import threading
import pandas as pd
from PIL import Image, ImageTk
import urllib.request
from tkinter import ttk
from web_scraping import scrapeHolidify
from flight_function import flight_information


def search_button_click():
    try:
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

def fetch_flight_information(source, dest, arrival, departure):
    flight_list = flight_information(source, dest, arrival, departure)
    flight_listbox = tk.Listbox(root, height=10, width=100)
    flight_listbox.grid(row=7, column=1,columnspan=2)
    print(flight_list)
    for flights in flight_list:
        print(flights)
        flight_listbox.insert(tk.END, flights)


def fetch_web_scraping(dest):
    hotel_list = scrapeHolidify(dest.lower())
    n = 10
    hotel_listbox = tk.Listbox(root, height=n, width=100)
    hotel_listbox.grid(row=9, column=1,columnspan=2)

    for hotel in hotel_list:
        name, price = hotel
        hotel_listbox.insert(tk.END, name + "---- Total Price :"+price)


'''
Funtion which returns a list of attractions with details based on the destination provided
:param dest:
:return:
'''
def fetch_attraction_places(dest):

    df = pd.read_csv('data/tourist_attractions.csv')


    # filter on attraction and state
    attraction_filter = df['attraction'].str.contains(dest, case=False)
    state_filter = df['state'].str.contains(dest, case=False)
    if attraction_filter.any():
        test_df = df[attraction_filter]
        state = test_df['state'].iloc[0]
        print(state)
        filtered_df = df[df['state'] == state]
    else:
        filtered_df = df[state_filter]

    result_text = ""

    for index, row in filtered_df.iterrows():
        attraction = row['attraction']
        ideal_duration = row["ideal_duration"]
        best_time = row["best_time"]
        description = row["description"]
        url_match = row["url_match"]

        # Load the image from the URL
        print(url_match)
        headers = {'User-Agent': 'Mozilla/5.0'}
        req = urllib.request.Request(url_match, headers=headers)
        with urllib.request.urlopen(req) as url:
            img_data = url.read()
        image = Image.open(BytesIO(img_data))

        # Append the values to the result label
        result_text += "attraction: " + attraction + "\n" + "Ideal duration: " + str(
            ideal_duration) + "\n" + "Best time to visit: " + str(best_time) + "\n" \
                       + "Description: " + str(description) + "-------------------------------------\n"

        # Resize the image and convert it to a Tkinter-compatible format
        image = image.resize((200, 200))
        photo = ImageTk.PhotoImage(image)

        result_label.image_create(tk.END, image=photo)

        result_label.configure(state="normal")
        result_label.delete("1.0", tk.END)  # clear the existing content
        result_label.insert(tk.END, result_text)  # insert the new content
        result_label.configure(state="disabled")

    scrollbar.config(command=result_label.yview)



root = tk.Tk()
root.geometry("700x1000")
root.title("Travel Planner")

header_label = ttk.Label(root, text="My Travel Planner", font=("Arial", 24, "bold"), anchor="center")
header_label.grid(row=0, column=0, columnspan=3, sticky='nsew',pady=5)
header_label.configure(anchor='center')

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
