""" A Program that read GDP in csv and render XY plot 
for yearly GDP for a specified list of countries
"""  

import csv
import pygal

def read_csv_as_nested_dict(filename, keyfield, separator, quote):
    """
    Inputs:
      filename  - Name of CSV file
      keyfield  - Field to use as key for rows
      separator - Character that separates fields
      quote     - Character used to optionally quote fields

    Output:
      Returns a dictionary of dictionaries where the outer dictionary
      maps the value in the key_field to the corresponding row in the
      CSV file.  The inner dictionaries map the field names to the
      field values for that row.
    """
    nested_dict = {}
    with open(filename, newline='') as csv_file:
        # This function converts a csv file in a dictionary 
        reader = csv.DictReader(csv_file, quotechar=quote, delimiter=separator)
        for row in reader:
            nested_dict[row[keyfield]] = {
                fieldName: fieldValue 
                for fieldName, fieldValue in row.items()}
    return nested_dict

def build_plot_values(gdpinfo, gdpdata):
    """
    Inputs:
      gdpinfo - GDP data information dictionary
      gdpdata - A single country's GDP stored in a dictionary whose
                keys are strings indicating a year and whose values
                are strings indicating the country's corresponding GDP
                for that year.

    Output: 
      Returns a list of tuples of the form (year, GDP) for the years
      between "min_year" and "max_year", inclusive, from gdpinfo that
      exist in gdpdata.  The year will be an integer and the GDP will
      be a float.
    """
    gdp_list_of_tuples = []
    for field_name, gdp in gdpdata.items():
        try:
            year = int(field_name)
            gdp = float(gdp)
        except ValueError:
            continue
        if gdpinfo['min_year'] <= year <= gdpinfo['max_year']:
            data = (year, gdp)
            gdp_list_of_tuples.append(data)
        else:
            continue  
    return gdp_list_of_tuples

def build_plot_dict(gdpinfo, country_list):
    """
    Inputs:
      gdpinfo      - GDP data information dictionary
      country_list - List of strings that are country names

    Output:
      Returns a dictionary whose keys are the country names in
      country_list and whose values are lists of XY plot values 
      computed from the CSV file described by gdpinfo.

      Countries from country_list that do not appear in the
      CSV file should still be in the output dictionary, but
      with an empty XY plot value list.
    """
    gdp_countries_data = {}
    gdpdata = read_csv_as_nested_dict(gdpinfo['gdpfile'], 
                                      gdpinfo['country_name'], 
                                      gdpinfo['separator'], 
                                      gdpinfo['quote'])
    for country in country_list:
        match = gdpdata.get(country)
        if match is not None:
            gdp_countries_data[country] = build_plot_values(gdpinfo, gdpdata[country])
        else: 
            gdp_countries_data[country] = []
    return gdp_countries_data

def render_xy_plot(gdpinfo, country_list, plot_file):
    """
    Inputs:
      gdpinfo      - GDP data information dictionary
      country_list - List of strings that are country names
      plot_file    - String that is the output plot file name

    Output:
      Returns None.

    Action:
      Creates an SVG image of an XY plot for the GDP data
      specified by info for the countries in country_list.
      The image will be stored in a file named by plot_file.
    """   
    gdp_countries_data = build_plot_dict(gdpinfo, country_list)
    xy_chart = pygal.XY(width=600, 
                        height=320, 
                        x_title='Year', 
                        y_title='GDP in current US dollars')
    xy_chart.title = plot_file
    for country in country_list:
        xy_chart.add(country, gdp_countries_data[country])
    xy_chart.render_in_browser()

gdpinfo = {
        "gdpfile": "isp_gdp.csv",        # Name of the GDP CSV file
        "separator": ",",                # Separator character in CSV file
        "quote": '"',                    # Quote character in CSV file
        "min_year": 1960,                # Oldest year of GDP data in CSV file
        "max_year": 2015,                # Latest year of GDP data in CSV file
        "country_name": "Country Name",  # Country name field name
        "country_code": "Country Code"   # Country code field name
    }

gdpdata = read_csv_as_nested_dict(gdpinfo['gdpfile'], gdpinfo['country_name'], gdpinfo['separator'], gdpinfo['quote'])
prepare_data = build_plot_values(gdpinfo, gdpdata["Andorra"])
build_to_plot = build_plot_dict(gdpinfo,["Venezuela"])
render_xy_plot(gdpinfo, ["Andorra", "Canada", "Aruba", "Bolivia", "United Arab Emirates"], 'Plot of GDP for select countries spanning 1960 to 2015')

