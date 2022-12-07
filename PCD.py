import tkinter as tk
from tkinter import *
from tkinter import ttk
import requests
import json
import pandas as pd
import webbrowser
import datetime
import os
from pathlib import Path


# Creates Frame
root = tk.Tk()
root.geometry("1200x700")
root.title("Potential Client Data")
# End Frame creation

c_city = tk.StringVar(value="Gainesville")
c_num=tk.StringVar(value="2")
c_offset=tk.StringVar(value="200")
c_min_price=tk.StringVar(value="150000")
c_max_price=tk.StringVar(value="350000")
c_seller = tk.IntVar(value=0)
c_seller2 = tk.IntVar(value=0)
c_seller3 = tk.IntVar(value=0)

input_text1=tk.StringVar()
seller_city = tk.StringVar(value="Gainesville")
input_text2=tk.StringVar()

year = int((datetime.datetime.now()).strftime("%Y"))
year_folder = str((datetime.datetime.now()).strftime("%Y"))
month = str((datetime.datetime.now()).strftime("%b"))
date = str((datetime.datetime.now()).strftime("%d"))

buyer_ph = "1) Buyers"
seller_ph = "2) Sellers"
personal_ph = "3) Personal"

# dejaboomcya@gmail.com
key1 = "API_STRING" #Not provided

# apitakeemail1@gmail.com
key2 = "API_STRING" #Not provided

#apitakeemail2@gmail.com
key3 = "API_STRING" #Not provided

# Method Creation

def got_clicked():
  city = c_city.get()
  num = c_num.get()
  offset = c_offset.get()
  min_price = c_min_price.get()
  max_price = c_max_price.get()
  seller = c_seller.get()
  seller2 = c_seller2.get()
  seller3 = c_seller3.get()
  
  seller_runs = 1

  myfile = Path(month + '_buyer.txt')
  myfile.touch(exist_ok=True)
  r = open(month + '_buyer.txt', 'r+')
  oldruns = (r.read())
  if oldruns == '':
    r.seek(0)
    r.write('1')
    buyer_runs = 1
  else:
    oldruns = int(oldruns)
    buyer_runs = oldruns + 1
    r.seek(0)
    r.write(str(buyer_runs))
  r.close()

  if seller == 1 or seller2 == 1 or seller3 == 1:
      myfile = Path(month + '_seller.txt')
      myfile.touch(exist_ok=True)
      r = open(month + '_seller.txt', 'r+')
      oldruns = (r.read())
      if oldruns == '':
        r.seek(0)
        r.write('1')
        seller_runs = 1
      else:
        oldruns = int(oldruns)
        seller_runs = oldruns + 1
        r.seek(0)
        r.write(str(seller_runs))
        r.close()
      if seller_runs > 3000:
        seller = 0

  # End instantiation

  # Create directory to hold excel
  if not os.path.exists('../' + personal_ph):
      os.makedirs('../' + personal_ph)
  if not os.path.exists('../' + personal_ph + "/" + month):
      os.makedirs('../' + personal_ph + "/" + month)
  if not os.path.exists('../' + personal_ph + "/" + month + '/' + date):
      os.makedirs('../' + personal_ph + "/" + month + '/' + date)

  if not os.path.exists('../' + buyer_ph):
      os.makedirs('../' + buyer_ph)
  if not os.path.exists('../' + buyer_ph + "/" + month):
      os.makedirs('../' + buyer_ph + "/" + month)
  if not os.path.exists('../' + buyer_ph + "/" + month + '/' + date):
      os.makedirs('../' + buyer_ph + "/" + month + '/' + date)

  if not os.path.exists('../' + seller_ph):
      os.makedirs('../' + seller_ph)
  if not os.path.exists('../' + seller_ph + "/" + month):
      os.makedirs('../' + seller_ph + "/" + month)
  if not os.path.exists('../' + seller_ph + "/" + month + '/' + date):
      os.makedirs('../' + seller_ph + "/" + month + '/' + date)
  # End directory creation

  # Names excel sheets
  page = ("Personal-" + str(city)+'-'+str((datetime.datetime.now()).strftime(
      "%b-%d-%Y_%H-%M-%S"))+ '.xlsx')
  page_csv = ("Recent_Buyers-" + str(city)+'-'+
              str((datetime.datetime.now()).strftime("%b-%d-%Y_%H-%M-%S"))
              + '.xlsx')
  page_seller = ("Recent_Sellers-" + str(city)+'-'+
                 str((datetime.datetime.now()).strftime("%b-%d-%Y_%H-%M-%S"))+
                 '.xlsx')
  # End naming

  if (seller == 1 & seller_runs <= 1000):
    key = key1
  elif (seller == 1 & seller_runs > 1000 & seller_runs <= 2000):
    key = key2
  elif (seller == 1 & seller_runs > 2000 & seller_runs <= 3000):
    key = key3

  ## Creating excel sheets with columns

  # Creates Excel Sheet for personal use
  writer = pd.ExcelWriter('../3) Personal/'+month+"/"+date+'/'+page, engine = 'xlsxwriter')
  cols = ['Address', 'City', 'State', 'Zip', 'Buy Date', 'Link']

  # Creates Excel Sheet for Buyers
  writer_csv = pd.ExcelWriter('../1) Buyers/' +month+"/"+date+'/' + page_csv, engine = 'xlsxwriter')
  cols_csv = ['Address', 'City', 'State', 'Zip', 'First Name', 'Last Name',
              'Spouse First Name', 'Spouse Last Name']

  # Creates Excel Sheet for Sellers if selected
  if (seller == 1 or seller2 == 1 or seller3 == 1):
      writer_seller = pd.ExcelWriter('../2) Sellers/' +month+"/"+date+'/' + page_seller, engine = 'xlsxwriter')
      cols_seller = ['Full Name', 'Age', 'Gender', 'Education', 'Household Income',
                     'Marital Status', 'Children?', 'Senior?', 'Phone#', 'Email']

  ## End excel sheet creation

  ## Creating dataframes

  # Creates Dataframe for Personal spreadsheet
  df = pd.DataFrame(columns = cols)

  # Creates Dataframe for csv
  df_csv = pd.DataFrame(columns = cols_csv)

  # Creates Dataframe for seller if selected
  if (seller == 1 or seller2 == 1 or seller3 == 1):
      df_seller = pd.DataFrame(columns = cols_seller)

  ## End dataframe creation

  # Connects to Recently Sold Homes API and stores request
  url = "https://realty-in-us.p.rapidapi.com/properties/v2/list-sold"

  querystring = {"offset":str(offset),"limit":str(num),"city":str(city),
                 "state_code":"GA","sort":"sold_date","prop_type":"single_family",
                 "price_min":str(min_price),"price_max":str(max_price)}

  headers = {
      'x-rapidapi-host': "realty-in-us.p.rapidapi.com",
      'x-rapidapi-key': "API_STRING" #Not provided
      }

  response = requests.request("GET", url, headers=headers, params=querystring)

  data = response.json()

  count = len(data['properties'])
  # End Recently Sold Homes API

  # Stores data in dataframe x number of times
  # Also returns seller data if selected
  for x in range(0, int(count)):
    # Instantiate address parts for URL
    number = json.dumps(data['properties'][x]['address']['street_number'])
    line = json.dumps(data['properties'][x]['address']['street'])
    suffix = json.dumps(data['properties'][x]['address']['street_suffix'])
    city1 = json.dumps(data['properties'][x]['address']['city'])

    city2 = str(city)

    if (city2 == 'Gainesville' or city == 'Flowery Branch' or city == 'Braselton' or city == 'Cumming'):
      number = str(number).replace('"', '')
      line = line + " "

      for r in ("null",""),(" N ", " North "),(" E ", " East "),(" S ", " South "),(" W ", " West "),(" NE ", " Northeast "),(" SE ", " Southeast "),(" SW ", " Southwest "),(" NW ", " Northwest "):
          line.replace(*r)
      for r in (" ", '+'), ('"', ''), ('[', ''), (']', ''), ('%', ''),("'\'", ''), ("'", ''):
          number = number.replace(*r)
          line = line.replace(*r)
          suffix = suffix.replace(*r)
      for r in ("null",""),("St", "Street"),("Rd", "Road"),("Dr", "Drive"),("Ave", "Avenue"),("Ct", "Court"),("Pl", "Place"),("Hwy", "Highway"),("Bnd", "Bend"),("Trl", "Trail"),("Pkwy", "Parkway"),("Ln", "Lane"),("Ter", "Terrace"),("Cir", "Circle"),("Rdg", "Ridge"),("Xing","Crossing"),("Cv", "Cove"),("Apt", "Apartment"),(" ", '+'), ('"', ''), ('[', ''), (']', ''),('%', ''), ("'\'", ''), ("'", ''):
          suffix = suffix.replace(*r)

      total = number + "+" + line + suffix

      google = "https://qpublic.schneidercorp.com/Search?q=" + str(total)
    
    # End instantiation

    # Creates Hyperlink in buyer excel sheet for Hall County + more
      hyper = "HYPERLINK("
    
      link = "=" + hyper + '"' + google + '"' + ')'
    else:
      link = ''
    # End Hyperlink creation
    
    # Dataframe for Personal Spreadsheet
    df.loc[x] = [(data['properties'][x]['address']['line']),
                 (data['properties'][x]['address']['city']),
                 (data['properties'][x]['address']['state_code']),
                 (data['properties'][x]['address']['postal_code']),
                 (data['properties'][x]['last_update']),
                 link]
    # End Personal Dataframe

    # Dataframe for csv
    df_csv.loc[x] = [(data['properties'][x]['address']['line']),
                     (data['properties'][x]['address']['city']),
                     (data['properties'][x]['address']['state_code']),
                     (data['properties'][x]['address']['postal_code']),
                      "", "", "", ""
                    ]
    # End csv dataframe

    # Gets data for API query
    seller_line = str(data['properties'][x]['address']['line'])
    seller_city = str(data['properties'][x]['address']['city'])
    seller_state = str(data['properties'][x]['address']['state_code'])
    seller_zip = str(data['properties'][x]['address']['postal_code'])
    # End API query data
    
    # Runs seller API if checked
    if(seller == 1):# & seller_runs <= 3000):
        # Connects to Demographics API and stores request
        seller_url = "https://personator2.p.rapidapi.com/v3/WEB/ContactVerify/doContactVerify"

        seller_querystring = {"act":"check,verify,append,move",
                              "state":seller_state,
                              "format":"json",
                              "a1":seller_line,
                              "postal":seller_zip,
                              "city":seller_city}

        seller_headers = {
            'x-rapidapi-host': "personator2.p.rapidapi.com",
            'x-rapidapi-key': "API_STRING" #Not provided
            }

        seller_response = requests.request("GET", seller_url,
                                           headers=seller_headers,
                                           params=seller_querystring)

        seller_data = seller_response.json()
        # End Demographics API

        # Calculates seller age based off of BD
        DOB = str(seller_data['Records'][0]['DateOfBirth'])
        seller_DOB = DOB[0:4]
        if not seller_DOB == ' ' or seller_DOB == '':
            DOB = int(seller_DOB)
        if (DOB == ' ' or ''):
            age = ''
        else:
            age = year - DOB
        # Ends calculation
        
        # Dataframe for Seller Spreadsheet
        df_seller.loc[x] = [(seller_data['Records'][0]['NameFull']),
                            (age),
                            (seller_data['Records'][0]['DemographicsGender']),
                            (seller_data['Records'][0]['Education']),
                            (seller_data['Records'][0]['HouseholdIncome']),
                            (seller_data['Records'][0]['MaritalStatus']),
                            (seller_data['Records'][0]['PresenceOfChildren']),
                            (seller_data['Records'][0]['PresenceOfSenior']),
                            (seller_data['Records'][0]['PhoneNumber']),
                            (seller_data['Records'][0]['EmailAddress'])
                            ]
    elif(seller2 == 1):# & seller_runs <= 3000):
        # Connects to Demographics API and stores request
        seller_url = "https://personator2.p.rapidapi.com/v3/WEB/ContactVerify/doContactVerify"

        seller_querystring = {"act":"check,verify,append,move",
                              "state":seller_state,
                              "format":"json",
                              "a1":seller_line,
                              "postal":seller_zip,
                              "city":seller_city}

        seller_headers = {
            'x-rapidapi-host': "personator2.p.rapidapi.com",
            'x-rapidapi-key': "API_STRING" #Not provided
            }

        seller_response = requests.request("GET", seller_url,
                                           headers=seller_headers,
                                           params=seller_querystring)

        seller_data = seller_response.json()
        # End Demographics API

        # Calculates seller age based off of BD
        DOB = str(seller_data['Records'][0]['DateOfBirth'])
        seller_DOB = DOB[0:4]
        if not seller_DOB == ' ' or seller_DOB == '':
            DOB = int(seller_DOB)
        if (DOB == ' ' or ''):
            age = ''
        else:
            age = year - DOB
        # Ends calculation
        
        # Dataframe for Seller Spreadsheet
        df_seller.loc[x] = [(seller_data['Records'][0]['NameFull']),
                            (age),
                            (seller_data['Records'][0]['DemographicsGender']),
                            (seller_data['Records'][0]['Education']),
                            (seller_data['Records'][0]['HouseholdIncome']),
                            (seller_data['Records'][0]['MaritalStatus']),
                            (seller_data['Records'][0]['PresenceOfChildren']),
                            (seller_data['Records'][0]['PresenceOfSenior']),
                            (seller_data['Records'][0]['PhoneNumber']),
                            (seller_data['Records'][0]['EmailAddress'])
                            ]
    elif(seller3 == 1):# & seller_runs <= 3000):
        # Connects to Demographics API and stores request
        seller_url = "https://personator2.p.rapidapi.com/v3/WEB/ContactVerify/doContactVerify"

        seller_querystring = {"act":"check,verify,append,move",
                              "state":seller_state,
                              "format":"json",
                              "a1":seller_line,
                              "postal":seller_zip,
                              "city":seller_city}

        seller_headers = {
            'x-rapidapi-host': "personator2.p.rapidapi.com",
            'x-rapidapi-key': "API_STRING" #Not provided
            }

        seller_response = requests.request("GET", seller_url,
                                           headers=seller_headers,
                                           params=seller_querystring)

        seller_data = seller_response.json()
        # End Demographics API

        # Calculates seller age based off of BD
        DOB = str(seller_data['Records'][0]['DateOfBirth'])
        seller_DOB = DOB[0:4]
        if not seller_DOB == ' ' or seller_DOB == '':
            DOB = int(seller_DOB)
        if (DOB == ' ' or ''):
            age = ''
        else:
            age = year - DOB
        # Ends calculation
        
        # Dataframe for Seller Spreadsheet
        df_seller.loc[x] = [(seller_data['Records'][0]['NameFull']),
                            (age),
                            (seller_data['Records'][0]['DemographicsGender']),
                            (seller_data['Records'][0]['Education']),
                            (seller_data['Records'][0]['HouseholdIncome']),
                            (seller_data['Records'][0]['MaritalStatus']),
                            (seller_data['Records'][0]['PresenceOfChildren']),
                            (seller_data['Records'][0]['PresenceOfSenior']),
                            (seller_data['Records'][0]['PhoneNumber']),
                            (seller_data['Records'][0]['EmailAddress'])
                            ]
        # Ends Seller dataframe
        print(df_seller)
        
      
  # Writes dataframe to excel sheets and saves them
  df.to_excel(writer, sheet_name=str(city), index=False)
  for column in df:
      column_width = max(df[column].astype(str).map(len).max(), len(column))
      col_index = df.columns.get_loc(column)
      writer.sheets[str(city)].set_column(col_index, col_index, column_width)
  writer.save()

  df_csv.to_excel(writer_csv, sheet_name=str(city), index=False)
  for column1 in df_csv:
      column_width = max(df_csv[column1].astype(str).map(len).max(), len(column1))
      col_index = df_csv.columns.get_loc(column1)
      writer_csv.sheets[str(city)].set_column(col_index, col_index, column_width)
  writer_csv.save()

  if(seller == 1 or seller2 == 1 or seller3 == 1):
      df_seller.to_excel(writer_seller, sheet_name=str(city), index=False)
      #for column2 in df_seller:
      #    column_width = max(df_seller[column2].astype(str).map(len).max(), len(column2))
      #    col_index = df_seller.columns.get_loc(column2)
      #    writer_seller.sheets[str(city)].set_column(col_index, col_index, column_width)
      writer_seller.save()
  print("Done")
  # End dataframe writing

def got_clicked1():
  line = input_text1.get()
  seller_city1 = seller_city.get()
  zip_code = input_text2.get()

  myfile = Path(month + '_seller.txt')
  myfile.touch(exist_ok=True)
  r = open(month + '_seller.txt', 'r+')
  oldruns = (r.read())
  if oldruns == '':
    r.seek(0)
    r.write('1')
    seller_runs = 1
  else:
    oldruns = int(oldruns)
    seller_runs = oldruns + 1
    r.seek(0)
    r.write(str(seller_runs))
    r.close()
  if seller_runs > 3000:
    seller = 0

  if not os.path.exists('../' + seller_ph):
    os.makedirs('../' + seller_ph)
  if not os.path.exists('../' + seller_ph + "/" + month):
    os.makedirs('../' + seller_ph + "/" + month)
  if not os.path.exists('../' + seller_ph + "/" + month + '/' + date):
    os.makedirs('../' + seller_ph + "/" + month + '/' + date)

  page_seller = ("Recent_Sellers-" + str(seller_city1)+'-'+
                 str((datetime.datetime.now()).strftime("%b-%d-%Y_%H-%M-%S"))+
                 '.xlsx')

  writer_seller = pd.ExcelWriter('../2) Sellers/' +month+"/"+date+'/' + page_seller, engine = 'xlsxwriter')
  cols_seller = ['Full Name', 'Age', 'Gender', 'Education', 'Household Income',
                 'Marital Status', 'Children?', 'Senior?', 'Phone#', 'Email']
  
  df_seller = pd.DataFrame(columns = cols_seller)

  if (seller_runs <= 1000):
      key = key1
  elif (seller_runs > 1000 & seller_runs <= 2000):
      key = key2
  elif (seller_runs > 2000 & seller_runs <= 3000):
      key = key3

  seller_url = "https://personator2.p.rapidapi.com/v3/WEB/ContactVerify/doContactVerify"

  seller_querystring = {"act":"check,verify,append,move",
                        "state":"GA",
                        "format":"json",
                        "a1":line,
                        "postal":zip_code,
                        "city":seller_city1}

  seller_headers = {
      'x-rapidapi-host': "personator2.p.rapidapi.com",
      'x-rapidapi-key': key
      }

  seller_response = requests.request("GET", seller_url,
                                     headers=seller_headers,
                                     params=seller_querystring)

  seller_data = seller_response.json()
  # End Demographics API

  # Calculates seller age based off of BD
  DOB = str(seller_data['Records'][0]['DateOfBirth'])
  seller_DOB = DOB[0:4]
  if not seller_DOB == ' ' or seller_DOB == '':
      DOB = int(seller_DOB)
  if (DOB == ' ' or ''):
      age = ''
  else:
      age = year - DOB
  # Ends calculation
  
  # Dataframe for Seller Spreadsheet
  df_seller.loc[x] = [(seller_data['Records'][0]['NameFull']),
                      (age),
                      (seller_data['Records'][0]['DemographicsGender']),
                      (seller_data['Records'][0]['Education']),
                      (seller_data['Records'][0]['HouseholdIncome']),
                      (seller_data['Records'][0]['MaritalStatus']),
                      (seller_data['Records'][0]['PresenceOfChildren']),
                      (seller_data['Records'][0]['PresenceOfSenior']),
                      (seller_data['Records'][0]['PhoneNumber']),
                      (seller_data['Records'][0]['EmailAddress'])
                      ]

  df_seller.to_excel(writer_seller, sheet_name=str(seller_city1), index=False)
  for column3 in df_seller:
      column_width = max(df_seller[column3].astype(str).map(len).max(), len(column3))
      col_index = df_seller.columns.get_loc(column3)
      writer_seller.sheets[str(seller_city1)].set_column(col_index, col_index, column_width)
  writer_seller.save()
  print("Done")

# End Method Creation

# Instantiate Labels
ix = 33
ix2 = 37
iy = 0

x = 15
x2 = 50
y = 30

title_label = ttk.Label(root, text="Potential Customer Data (Buyer & Seller if chosen)", font = ("Helvetica 15")).grid(column=0, row=0, columnspan=2, sticky=tk.W, padx=x)
space_label = ttk.Label(root, text=" ").grid(column = 0, row = 1)
label1 = ttk.Label(root, text="Choose City: ", font = ("Times New Roman", 15)).grid(column=0, row=2, sticky=tk.W, padx=x, pady=y)
label2 = ttk.Label(root, text="Results to Display (1-200): ", font = ("Times New Roman", 15)).grid(column=0, row=3, sticky=tk.W, padx=x, pady=y)
label3 = ttk.Label(root, text="Offset of Results (1-500): ", font = ("Times New Roman", 15)).grid(column=0, row=4, sticky=tk.W, padx=x, pady=y)
label4 = ttk.Label(root, text="Offset of Results ($100k-3 Million): ", font = ("Times New Roman", 15)).grid(column=0, row=5, sticky=tk.W, padx=x, pady=y)
label5 = ttk.Label(root, text="Offset of Results ($101k-5 Million): ", font = ("Times New Roman", 15)).grid(column=0, row=6, sticky=tk.W, padx=x, pady=y)

title_label2 = ttk.Label(root, text="Potential Customer Data (Seller only)", font = ("Helvetica 15")).grid(column=3, row=0, columnspan=2, sticky=tk.W, padx=x2)
label6 = ttk.Label(root, text="Address Line: ", font = ("Times New Roman", 15)).grid(column=3, row=2, sticky=tk.W, padx=x2, pady=y)
label7 = ttk.Label(root, text="City: ", font = ("Times New Roman", 15)).grid(column=3, row=3, sticky=tk.W, padx=x2, pady=y)
label9 = ttk.Label(root, text="Zip: ", font = ("Times New Roman", 15)).grid(column=3, row=4, sticky=tk.W, padx=x2, pady=y)
# End Label instantiation

# Start Buyer & Seller
chosen_city = ttk.Combobox(root, width=30, textvariable=c_city)

chosen_city['values'] = ("Gainesville",
                     "Buford",
                     "Cumming",
                     "Flowery Branch",
                     "Braselton")

chosen_city.grid(column=1, row=2, sticky=tk.E, padx=x, pady=y)

results = ttk.Spinbox(root, from_=1, to=200, textvariable=c_num, wrap=True)
results.grid(column=1, row=3, sticky=tk.E, padx=x, pady=y, ipadx=ix, ipady=iy)

offset = ttk.Spinbox(root, from_=1, to=500, textvariable=c_offset, wrap=True)
offset.grid(column=1, row=4, sticky=tk.E, padx=x, pady=y, ipadx=ix, ipady=iy)

min_price = ttk.Spinbox(root, from_=100000, to=3000000, textvariable=c_min_price, wrap=True)
min_price.grid(column=1, row=5, sticky=tk.E, padx=x, pady=y, ipadx=ix, ipady=iy)

max_price = ttk.Spinbox(root, from_=101000, to=5000000, textvariable=c_max_price, wrap=True)
max_price.grid(column=1, row=6, sticky=tk.E, padx=x, pady=y, ipadx=ix, ipady=iy)

c1 = ttk.Checkbutton(root, text="Return seller data? (max 1000 a month)", variable=c_seller, onvalue=1, offvalue=0)
c1.grid(column=0, row=7, sticky=tk.W, padx=x, pady=y, ipadx=ix, ipady=iy)

c2 = ttk.Checkbutton(root, text="Return seller data? (max 1000 a month)", variable=c_seller2, onvalue=1, offvalue=0)
c2.grid(column=1, row=7, sticky=tk.W, padx=x, pady=y, ipadx=ix, ipady=iy)

c3 = ttk.Checkbutton(root, text="Return seller data? (max 1000 a month)", variable=c_seller3, onvalue=1, offvalue=0)
c3.grid(column=0, row=8, sticky=tk.W, padx=x, pady=y, ipadx=ix, ipady=iy)

button1 = ttk.Button(root, text = 'Run', command = got_clicked)
button1.grid(column = 0, row =9, sticky=tk.W, padx=x, pady=y, ipadx=ix, ipady=iy)
# End Buyer & Seller

# Begin Seller only
entry1 = ttk.Entry(root, textvariable = input_text1, justify = LEFT)
entry1.grid(column=4, row=2, sticky=tk.E, padx=x, pady=y, ipadx=ix2, ipady=iy)

seller_chosen_city = ttk.Combobox(root, width=30, textvariable=seller_city)

seller_chosen_city['values'] = ("Gainesville",
                     "Buford",
                     "Cumming",
                     "Flowery Branch",
                     "Braselton")

seller_chosen_city.grid(column=4, row=3, sticky=tk.E, padx=x, pady=y)

entry1 = ttk.Entry(root, textvariable = input_text2, justify = LEFT)
entry1.grid(column=4, row=4, sticky=tk.E, padx=x, pady=y, ipadx=ix2, ipady=iy)

button2 = ttk.Button(root, text = 'Run', command = got_clicked1)
button2.grid(column = 3, row =8, sticky=tk.W, padx=x2, pady=y, ipadx=ix, ipady=iy)
# End Seller only

root.mainloop()
