import tkinter as tk
from pandas_datareader import data
import pandas as pd
import datetime as dt


# -----FUNCTIONS-----
# Function for selecting the date in the GUI pulling data from fields
def date_selection():
    date_error_text = "Date error, try again."
    date_accepted_text = "Dates Accepted."
    try:
        sy = int(start_year_field.get())
        sm = int(start_month_field.get())
        sd = int(start_day_field.get())
        ey = int(end_year_field.get())
        em = int(end_month_field.get())
        ed = int(end_day_field.get())
        start = dt.datetime(sy, sm, sd)
        end = dt.datetime(ey, em, ed)
        start_text = start.strftime('%m/%d/%Y')
        end_text = end.strftime('%m/%d/%Y')
        display_sd = tk.Text(height=1, width=10, bg='Light Grey')
        display_sd.grid(column=7, row=2)
        display_sd.insert(tk.END, start_text)
        display_sd.configure(state='disabled')
        display_ed = tk.Text(height=1, width=10, bg='Light Grey')
        display_ed.grid(column=7, row=3)
        display_ed.insert(tk.END, end_text)
        display_ed.configure(state='disabled')
        dates_label = tk.Label(text='Date Range: ')
        dates_label.grid(column=7, row=1)
        display_accept = tk.Text(height=1, width=25, bg='Light Grey')
        display_accept.grid(column=8, row=1)
        display_accept.insert(tk.END, date_accepted_text)
        display_accept.configure(state='disabled')
        return start, end
    except (ValueError, TypeError):
        display_error = tk.Text(height=1, width=25, bg='Light Grey')
        display_error.grid(column=8, row=1)
        display_error.insert(tk.END, date_error_text)
        display_error.configure(state='disabled')


# Function for pulling historical data for tickers to add to a dataframe.
def get_price():
    global nigo_ticker
    global appended_data
    global ticker_table

    ticker_error_text = "Add tickers to table"
    start, end = date_selection()
    raw_date = dt.datetime.now()
    date = raw_date.strftime("%m.%d.%Y")
    for i in ticker_table:
        try:
            web = data.DataReader(i, "yahoo", start, end)
            # web = web[['Adj Close']] # Limits output to adjusted closing price.
            web.insert(0, 'Ticker', i)
            # print(str(i))  # Used these lines when printing in terminal.
            # print(web)  # Used these lines when printing in terminal.
            appended_data.append(web)
        except:
            nigo_ticker.append(i)
            nigo_ticker_display = tk.Text(height=3, width=20, bg='light grey')
            nigo_ticker_display.grid(column=3, row=7)
            nigo_ticker_display.insert(tk.END, nigo_ticker)
            nigo_ticker_title = tk.Label(text="NIGO Ticker: ", justify='right')
            nigo_ticker_title.grid(column=2, row=7)
    try:
        appended_data = pd.concat(appended_data, axis=0)
        with open('ticker_table_' + date + '.csv', 'a') as file:
            appended_data.to_csv(file, mode='a')
    except AttributeError:
        with open('ticker_table_' + date + '.csv', 'a') as file:
            appended_data.to_csv(file, mode='a')
    except ValueError:
        display = tk.Text(height=5, width=20, bg='Light Grey')
        display.grid(column=3, row=6)
        display.insert(tk.END, ticker_error_text)
        display.configure(state='disabled')
    except TypeError:
        with open('ticker_table_' + date + '.csv', 'a') as file:
            appended_data.to_csv(file, mode='a')
            
    view_instructions = tk.Label(text='Results exported to CSV file.\nNIGO tickers were not included.', justify='left')
    view_instructions.grid(column=0, row=8)



# Function to add tickers to ticker_table list
def ticker_table_add():
    global ticker_table
    ticker_add = (ticker_field.get().upper())
    if ticker_add not in ticker_table:
        ticker_table.append(ticker_add)
    # print(ticker_table)
    display = tk.Text(height=5, width=20, bg='Light Grey')
    display.grid(column=3, row=6)
    display.insert(tk.END, ticker_table)
    display.configure(state='disabled')
    display_title = tk.Label(text="Ticker Table: ", justify='right')
    display_title.grid(column=2, row=6)


# Function to remove tickers from ticker_table list
def ticker_table_remove():
    global ticker_table
    ticker_remove = (ticker_field.get().upper())
    try:
        ticker_table.remove(ticker_remove)
        display = tk.Text(height=5, width=20, bg='Light Grey')
        display.grid(column=3, row=6)
        display.insert(tk.END, ticker_table)
        display.configure(state='disabled')
    except ValueError:
        display = tk.Text(height=5, width=20, bg='Light Grey')
        display.grid(column=3, row=6)
        display.insert(tk.END, ticker_table)
        display.configure(state='disabled')


# ----------MAIN PROGRAM----------
# -----LISTS-----
appended_data = []
ticker_table = []
nigo_ticker = []

# -----WINDOW-----
window = tk.Tk()
window.title("Historical Pricing App")
window.geometry("1000x500")

# -----LABELS-----
# Title label
title = tk.Label(text="Pricing History", font=("Helvetica", 16))
title.grid(column=3, row=0)

# Footer label, located lower right of window
footer = tk.Label(text="Created by: NoWorriesDevelopment.com\nRelease date: 2/26/2019\nHakunaMatata1988@outlook.com", justify='left')
footer.grid(column=7, row=20)

# Date selection labels
start_year_label = tk.Label(text="Start Year: ")
start_year_label.grid(column=0, row=2)

start_month_label = tk.Label(text="Start Month: ")
start_month_label.grid(column=2, row=2)

start_day_label = tk.Label(text="Start Day: ")
start_day_label.grid(column=5, row=2)

end_year_label = tk.Label(text="End Year: ")
end_year_label.grid(column=0, row=3)

end_month_label = tk.Label(text="End Month: ")
end_month_label.grid(column=2, row=3)

end_day_label = tk.Label(text="End Day: ")
end_day_label.grid(column=5, row=3)

# Ticker selection label
ticker_add_label = tk.Label(text="Ticker Symbol")
ticker_add_label.grid(column=0, row=4)

# Instructions label
instructions = "Step 1. Enter desired date range and submit.\nStep 2. Add tickers to table.\nStep 3. Request tickers."
instructions_label = tk.Label(text=instructions, justify='left')
instructions_label.grid(column=0, row=1)


# -----ENTRY FIELDS-----
# Date selection fields
start_year_field = tk.Entry(width=5)
start_year_field.grid(column=1, row=2)

start_month_field = tk.Entry(width=3)
start_month_field.grid(column=3, row=2)

start_day_field = tk.Entry(width=3)
start_day_field.grid(column=6, row=2)

end_year_field = tk.Entry(width=5)
end_year_field.grid(column=1, row=3)

end_month_field = tk.Entry(width=3)
end_month_field.grid(column=3, row=3)

end_day_field = tk.Entry(width=3)
end_day_field.grid(column=6, row=3)

# Ticker add field
ticker_field = tk.Entry(width=7)
ticker_field.grid(column=1, row=4)

# -----BUTTONS-----
add_ticker_button = tk.Button(text="Add Ticker", bg="Green", command=ticker_table_add)
add_ticker_button.grid(column=2, row=4)

delete_ticker_button = tk.Button(text='Remove Ticker', bg='Red', command=ticker_table_remove)
delete_ticker_button.grid(column=3, row=4)

date_submit_button = tk.Button(text="Submit Date", bg="Yellow", command=date_selection)
date_submit_button.grid(column=8, row=3)

master_submit_button = tk.Button(text="Request Tickers", bg='Light Green', justify='left', command=get_price)
master_submit_button.grid(column=0, row=7)


# Insert executable below here, above this line is the GUI design.

# Main loop function
window.mainloop()

print(ticker_table)
