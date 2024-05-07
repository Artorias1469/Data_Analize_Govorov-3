#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import json

def add_flight(destination, flight_number, aircraft_type):
    return {'название пункта назначения': destination,
            'номер рейса': flight_number,
            'тип самолета': aircraft_type}

def print_flights(flights):
    line = '+-{}-+-{}-+-{}-+'.format(
        '-' * 30,
        '-' * 20,
        '-' * 15
    )
    print(line)
    print('| {:^30} | {:^20} | {:^15} |'.format(
        "Название пункта назначения",
        "Номер рейса",
        "Тип самолета"
    ))
    print(line)

    for flight in flights:
        print('| {:<30} | {:<20} | {:<15} |'.format(
            flight.get('название пункта назначения', ''),
            flight.get('номер рейса', ''),
            flight.get('тип самолета', '')
        ))

    print(line)

def search_flights_by_aircraft_type(flights_list, search_aircraft_type):
    matching_flights = [flight for flight in flights_list if flight['тип самолета'] == search_aircraft_type]

    if matching_flights:
        print("\nРейсы, обслуживаемые самолетом типа {}: ".format(search_aircraft_type))
        print_flights(matching_flights)
    else:
        print(f"\nРейсов, обслуживаемых самолетом типа {search_aircraft_type}, не найдено.")

def save_to_json(filename, data):
    with open(filename, 'w', encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_from_json(filename):
    try:
        with open(filename, 'r', encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def main():
    parser = argparse.ArgumentParser(description="Flight Information Management System")
    parser.add_argument("-a", "--add-flight", action="store_true", help="Add a new flight")
    parser.add_argument("-p", "--print-flights", action="store_true", help="Print the list of flights")
    parser.add_argument("-s", "--search-by-type", help="Search flights by aircraft type")
    parser.add_argument("-f", "--file", default="flights.json", help="JSON file to load/save flight data")
    args = parser.parse_args()

    if args.add_flight:
        destination = input("Введите название пункта назначения: ")
        flight_number = input("Введите номер рейса: ")
        aircraft_type = input("Введите тип самолета: ")
        flight = add_flight(destination, flight_number, aircraft_type)
        flights_list = load_from_json(args.file)
        flights_list.append(flight)
        flights_list.sort(key=lambda x: x['название пункта назначения'])
        save_to_json(args.file, flights_list)

    elif args.print_flights:
        flights_list = load_from_json(args.file)
        print_flights(flights_list)

    elif args.search_by_type:
        flights_list = load_from_json(args.file)
        search_flights_by_aircraft_type(flights_list, args.search_by_type)

    else:
        parser.print_help()

if __name__ == '__main__':
    main()
