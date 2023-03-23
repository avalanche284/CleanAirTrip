import sys
import requests
import csv
import pytz
import json
from fpdf import FPDF
from datetime import datetime

API_KEY = "XXX"
# get air pollution url
BASE_URL = "http://api.openweathermap.org/data/2.5/air_pollution?"
# geocoding url
GEO_URL = "http://api.openweathermap.org/geo/1.0/direct?"

class PDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 14)
        self.cell(80)
        self.cell(30, 35, "CleanAirTrip Report", align="C")

    def add_current_time(self):
        UTC = pytz.utc
        datetime_utc = datetime.now(UTC)
        self.set_font("Helvetica", "", 7)
        self.cell(0, 0, f"{datetime_utc.strftime('%d/%m/%Y, %H:%M %Z')}", align="R")
        self.ln(30)

    def colored_table(self, headings, rows, col_widths=(7,33,20,40)):
        # Colors, line width and bold font:
        self.set_fill_color(98, 187, 69) # color of filling the header of a table
        self.set_text_color(255)
        self.set_draw_color(79, 149, 56) # color of lines in a table
        self.set_line_width(0.3)
        self.set_font("Helvetica", "B", 13)
        for col_width, heading in zip(col_widths, headings):
            self.cell(col_width, 7, heading, border=1, align="C", fill=True)
        self.ln()
        # Color and font restoration
        self.set_fill_color(208, 234, 200) # color of every other row
        self.set_text_color(0)
        self.set_font("Helvetica")
        fill = False
        for row in rows:
            self.cell(col_widths[0], 6, row[0], border="LR", align="L", fill=fill)
            self.cell(col_widths[1], 6, row[1], border="LR", align="L", fill=fill)
            self.cell(col_widths[2], 6, row[2], border="LR", align="C", fill=fill)
            self.cell(col_widths[3], 6, row[3], border="LR", align="C", fill=fill)
            self.ln()
            fill = not fill
        self.cell(sum(col_widths), 0, "", "T")
        self.ln(4)

    # text under the table
    def chapter_body(self, filepath):
        with open(filepath, "rb") as fh:
            txt = fh.read().decode("latin-1")
        self.set_font("Helvetica", size=12)
        # Printing justified text
        self.multi_cell(0, 5, txt)
        self.ln()

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "", 7)
        self.cell(0, 0, f"Page {self.page_no()} of {{nb}}", align="R")

#####

def main():
    create_csv(add_numbers(sort_AQIs(get_AQIs(get_coordinates()))))
    save_pdf()

#####

def get_coordinates():
    cities = []
    try:
        for i in sys.argv[1:]:
            city = i.casefold().title()
            response = requests.get(f"{GEO_URL}q={city}&appid={API_KEY}")
            data = response.json()
            latitude = data[0]["lat"]
            longitude = data[0]["lon"]
            coordinates = {}
            coordinates["city"] = city
            coordinates["latitude"] = latitude
            coordinates["longitude"] = longitude
            cities.append(coordinates)
        return cities
    except IndexError:
        sys.exit("The city you provided is not correct. Try again.")


def get_AQIs(given_cities):
    aqis = []
    for city in given_cities:
        lat = city["latitude"]
        lon = city["longitude"]
        response = requests.get(f"{BASE_URL}lat={lat}&lon={lon}&appid={API_KEY}")
        data = response.json()
        aqi = {}
        aqi["city"] = city["city"]
        aqi["aqi"] = data["list"][0]["main"]["aqi"]
        aqis.append(aqi)
    return aqis


def sort_AQIs(unsorted_aqis):
    sorted_aqis = sorted(unsorted_aqis, key=lambda d: d["aqi"])
    return sorted_aqis

def add_numbers(cities_aqis):
    j = 1
    for result in cities_aqis:
        result["No"] = j
        j = j + 1
        if result["aqi"] == 1:
            result["Qualitative name"] =  "Very low"
        elif result["aqi"] == 2:
            result["Qualitative name"] = "Low"
        elif result["aqi"] == 3:
            result["Qualitative name"] = "Medium"
        elif result["aqi"] == 4:
            result["Qualitative name"] = "High"
        elif result["aqi"] == 5:
            result["Qualitative name"] = "Very high"
    return cities_aqis

def create_csv(list_of_cities):
    with open("results.csv", "w") as file:
        writer = csv.DictWriter(file, fieldnames=["No", "City", "AQI", "Qualitative name"])
        writer.writerow({"No": "No", "City": "City", "AQI": "AQI", "Qualitative name": "Qualitative name"})
        for i in list_of_cities:
            writer.writerow({"No": i['No'], "City": i['city'], "AQI": i['aqi'], "Qualitative name": i['Qualitative name']})

def load_data_from_csv(csv_filepath):
    headings, rows = [], []
    with open(csv_filepath, encoding="utf8") as csv_file:
        for row in csv.reader(csv_file, delimiter=","):
            if not headings:  # extracting column names from first row
                headings = row
            else:
                rows.append(row)
    return headings, rows

def save_pdf():
    col_names, data = load_data_from_csv("results.csv")
    pdf = PDF()
    pdf.alias_nb_pages()     # get total page numbers
    pdf.add_page()
    pdf.add_current_time()
    pdf.colored_table(col_names, data)
    pdf.chapter_body("short_description.txt")
    print("The report was generated successfully!")
    pdf.output("CleanAirTrip.pdf")


if __name__ == "__main__":
    main()
