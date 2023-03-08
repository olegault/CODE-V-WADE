import sqlite3
from google_play_scraper import app
import numpy as np
import pycountry

address = '89 Kennedy Avenue, Office 201, 1077 Nicosia, Cyprus'

# split the address by comma
parts = address.split(',')

# extract the last part and remove any leading/trailing whitespace
country = parts[-1].strip()

print(country) # output: "Cyprus"


# get a list of all countries
all_countries = list(pycountry.countries)

# create a list of tuples with the country name and code
countries_list = [(country.name, country.alpha_2) for country in all_countries]

# sort the list by country name
countries_list.sort()

# create an HTML dropdown menu string
dropdown_menu = '<select name="country">'
for country in countries_list:
    dropdown_menu += '<option value="{0}">{1}</option>'.format(country[1], country[0])
dropdown_menu += '</select>'

print(dropdown_menu)