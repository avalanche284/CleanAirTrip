import pytest
import sys
import os.path
from project import get_coordinates, get_AQIs, sort_AQIs, \
    add_numbers, create_csv, load_data_from_csv, save_pdf

def main():
    test_get_coordinates_correct_1_city()
    test_get_coordinates_correct_2_cities()
    test_get_coordinates_error()
    test_get_AQIs()
    test_sort_AQIs()
    test_add_numbers()
    test_create_csv()
    test_load_data_from_csv()
    test_save_pdf()

def test_get_coordinates_correct_1_city(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["project.py", "Cupertino"])
    assert get_coordinates() == [
        {
            "city": "Cupertino",
            "latitude": 37.3228934,
            "longitude": -122.0322895,
        },
    ]
def test_get_coordinates_correct_2_cities(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["project.py", "Cupertino", "Boston"])
    assert get_coordinates() == [
        {
            "city": "Cupertino",
            "latitude": 37.3228934,
            "longitude": -122.0322895,
        },
        {
            "city": "Boston",
            "latitude": 42.3554334,
            "longitude": -71.060511,
        }
    ]

def test_get_coordinates_error(monkeypatch):
    with pytest.raises(IndexError):
        monkeypatch.setattr(sys, "argv", ["project.py", "Cuuuupertino"])
        raise IndexError

def test_get_AQIs():
    assert (get_AQIs([
        {
            'city': 'Cupertino',
            'latitude': 37.3228934,
            'longitude': -122.0322895
        }
    ]) in list_of_aqis) == True


list_of_aqis = [
    [{'city': 'Cupertino', 'aqi': 1}],
    [{'city': 'Cupertino', 'aqi': 2}],
    [{'city': 'Cupertino', 'aqi': 3}],
    [{'city': 'Cupertino', 'aqi': 4}],
    [{'city': 'Cupertino', 'aqi': 5}],
]

def test_sort_AQIs():
    assert sort_AQIs([
        {'city': 'Boston', 'aqi': 2},
        {'city': 'Cupertino', 'aqi': 1}
    ]) == [
        {'city': 'Cupertino', 'aqi': 1},
        {'city': 'Boston', 'aqi': 2}
    ]


def test_add_numbers():
    assert add_numbers([
        {'city': 'Cupertino', 'aqi': 1},
        {'city': 'Boston', 'aqi': 2}
    ]) == [
        {'city': 'Cupertino', 'aqi': 1, 'No': 1, 'Qualitative name': 'Very low'},
        {'city': 'Boston', 'aqi': 2, 'No': 2, 'Qualitative name': 'Low'},
    ]

def test_create_csv():
    create_csv([
        {'city': 'Cupertino', 'aqi': 1, 'No': 1, 'Qualitative name': 'Very low'},
        {'city': 'Boston', 'aqi': 2, 'No': 2, 'Qualitative name': 'Low'},
    ])
    assert os.path.exists("results.csv") == True


def test_load_data_from_csv():
    create_csv([
        {'city': 'Cupertino', 'aqi': 1, 'No': 1, 'Qualitative name': 'Very low'},
        {'city': 'Boston', 'aqi': 2, 'No': 2, 'Qualitative name': 'Low'},
    ])
    assert load_data_from_csv("results.csv") == (['No', 'City', 'AQI', 'Qualitative name'], [['1', 'Cupertino', '1', 'Very low'], ['2', 'Boston', '2', 'Low']])

def test_save_pdf():
    create_csv([
        {'city': 'Cupertino', 'aqi': 1, 'No': 1, 'Qualitative name': 'Very low'},
        {'city': 'Boston', 'aqi': 2, 'No': 2, 'Qualitative name': 'Low'},
    ])
    save_pdf()
    assert os.path.exists("CleanAirTrip.pdf") == True

if __name__ == "__main__":
    main()