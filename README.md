# CleanAirTrip
#### Take a deep breath of a clean air and travel around the world.
### Video Demo:  [HERE](https://youtu.be/J-pLkAlyziQ)
![screenshot of a pdf](preview.png)

## Description
I believe, the most valuable asset of every human being is his own health. It is extremely fragile, easy to break and often tough to get it back.

It is not uncommon to go on a holiday. Having my own health in mind and those who are close to me, I can make reasonable decision of where to go and spend time.

One of the things that I have an impact on in that case is a quality of air. On different areas, in different cities one can see varieties of how polluted the air is.

People developed ways, measurements of air pollution. Using indexes one can see differences in measurable ways. Having comparison one can see at which location an air is cleaner and at which is more polluted.

Using CleanAirTrip app you can compare cities around the world you consider visiting and see which of them is healthier for you. See AQI (Air Quality Index) and what it means in real-time. Save your comparison in pdf for future reference. Make an impact on what is most important in your life, and life of those who are close to you.

## What does the program do?
The application reads names of the cities provided by the user, checks air quiality in those locations, generates a comparison of them, lists the results and saves the outcome in a pdf file.

## Description #2
My project is implemented in Python. It is a simple, command-line interface application program.

The `main()` function is located in **project.py** file as well as other functions. They are nested on the same indentation level as main function (an exception is `load_data_from_csv()` function which is executable from `save_pdf()`. Each of the functions is accompanied by tests that can be executed with `pytest`, and they are located in **test_project.py**. The functions have the same name as custom functions, they are prepended with `test_` (for instance, `test_create_csv()` is a test for `create_csv()` function). Required `pip`-installable libraries are listed in `requirements.txt`.
## The manual
1. Open the terminal emulator (Terminal, Windows Console etc.).
2. `cd` to `project` directory.
3. Type the following:
```
python project.py
```
4. Type a space after typing `python project.py` and provide the names of cities, each of which should be separated by a space. If a name of a city has more than one word, it should be typed in quotes.
```
python project.py "San Francisco" "Las Vegas" Seattle Austin Chicago "New York" Miami London Barcelona Paris Milan Dubai Singapore Beijing Tokyo Sydney Melbourne "Buenos Aires" Brasilia "Mexico City"
```
5. Confirm by "enter" key.

The app confirms successful completion the task and saves pdf. If there was a misspell in city(ies) name(s), the program will inform about it.

## What files are included:
- project.py,
- test_project.py,
- CleanAirTrip.pdf,
- preview.png,
- requirements.txt,
- results.csv,
- short_description.txt.

### **project.py**
This is the main file of the app. The program uses OpenWeather's API. In order to access it you should provide your own. Mine was deleted after publication of the DEMO. In order to get one you can start a free account and put yours at the beginning of the program.
```
API_KEY = "your_API_key"
```
`get_coordinates()` has a task to get all of names of cities, besides mistakes with letter cases, check latitudes and longitudes of those cities (using OpenWeather's tool Geocoding API) and saves the result in list of dicts. In case any error in the city name provided by the user, it raises an IndexError.

`get_AQIs(given_cities)` uses another API to access real-time air pollution. It requires latitude and longitude from the previous function. It downloads data in json file, chooses only info about AQI and collect the data in list of dicts.

The sole purpose of `sort_AQIs(unsorted_aqis)` is, as its name suggest, sort cities and their AQIs in an ascending order.

According to the established order adding numbers occurs by `add_numbers(cities_aqis)`. Also "Qualitative name" is added.

`create_csv(list_of_cities)` generates a csv file of the results.

Creating pdf file is done by `save_pdf()` which uses fpdf2. The first line calls `load_data_from_csv(csv_filepath)` function which gets headers and rows from generated csv file. Current date and time is being added, next the header, table with the results and general description of AQI by fpdf2. The program prints a communicate about successful work and saves pdf file.

#### `class PDF(FPDF)`
Header of the file is constructed by `header()` function. `add_current_time()` prints current date and time in the top-right-hand corner. The actual compared results are displayed via `colored_table()`. `chapter_body()` takes care of the text - general description of AQI which takes the actual text from txt file. `footer()` prints the number of pages used to generate the pdf in the bottom right-hand corner.
### **test_project.py**
It performs basic tests on main file that can be executed via pytest.

The first three tests requires monkeypatching. Because of the fact that the CleanAirTrip app collects data via command-line interface this collection of data needs to be tested in other way than asking a user. `monkeypatch.setattr` dynamically modifies the behavior of `sys.argv`. It provides example data to the function, cities names like Cupertino or Boston.

The first two test functions compares data provided by API with those hardcoded here.

`test_get_coordinates_error(monkeypatch)` checks whether exception is raised.

Testing of choosing the correct data from API, of AQI, is done by `test_get_AQIs()`.list of lists with a city name and value of AQI is provided.

`test_sort_AQIs()` check the correctness of sorting by providing example data of Cupertino and Boston.

Checking whether numbers were added in the correct form is done in `test_add_numbers()`
function.

The construction of `test_create_csv()` and `test_save_pdf()` is the same: they checks whether the files were created after function execution.

`test_load_data_from_csv()` tests if the outcome of that function is list of headers and list of rows.

### **CleanAirTrip.pdf**
This is the generated pdf.

### **preview.png**
This is a screenshot of a pdf file.

### **requirements.txt**
In this file they are covered, line by line, pip-installable libraries that needs to be installed in order to run the app.

### **results.csv**
This is the file that is generated during execution of the app. It is just used by the program.

### **short_description.txt**
It covers general description under the main table in the pdf document.

## Design choices
During programming the app I was focused on implementing ideas and solutions that were mentioned during CS50P's course and many design choices were leaded by things and solutions that I have just learned and wanted to train them. But I did not relied on those solution, though! I need to search the Internet to look for other solutions, ready questions and answers on stack overflow etc. fdpf2 was used in one of the exercises. However, I needed to take time to learn creating tables in that tool.

A table is created using the most advanced one that was described in fpdf2's tutorial.

At first, city names were collected one by one by the program using:
```
while True:
    try:
        ...
    except IndexError: # when user prompts wrong value
        print("There is no such city. Please try again.")
        pass
    except EOFError: # when ^D
        print()
        return cities
```
However, I could not find at that time a way to test it. So I decided to change the solution as `sys.argv()` arguments.

And here I needed to learn monkeypatching. It was used in the first tests.

As this is quite short program and does not have many API calls I decided to not monkeypatch those. It does not take much time to perform tests. Geolocation of cities (latitude and longitude) does not change over the minutes so it is safe to have an active API call for it. This does not apply to AQI which can change very quickly and quite often. That is why the possible values were hardcoded in test_project.py
```
list_of_aqis = [
    [{'city': 'Cupertino', 'aqi': 1}],
    [{'city': 'Cupertino', 'aqi': 2}],
    [{'city': 'Cupertino', 'aqi': 3}],
    [{'city': 'Cupertino', 'aqi': 4}],
    [{'city': 'Cupertino', 'aqi': 5}],
]
```
This was CS50P!

<sub>The application is a final project on a CS50P course.</sub>
