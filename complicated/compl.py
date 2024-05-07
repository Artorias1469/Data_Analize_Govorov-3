#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import click

def add_flight(destination, flight_number, aircraft_type, flights_list):
    flight = {'название пункта назначения': destination,
              'номер рейса': flight_number,
              'тип самолета': aircraft_type}
    flights_list.append(flight)
    flights_list.sort(key=lambda x: x['название пункта назначения'])
    return flights_list

def print_flights(flights):
    line = '+-{}-+-{}-+-{}-+'.format(
        '-' * 30,
        '-' * 20,
        '-' * 15
    )
    click.echo(line)
    click.echo('| {:^30} | {:^20} | {:^15} |'.format(
        "Название пункта назначения",
        "Номер рейса",
        "Тип самолета"
    ))
    click.echo(line)

    for flight in flights:
        click.echo('| {:<30} | {:<20} | {:<15} |'.format(
            flight.get('название пункта назначения', ''),
            flight.get('номер рейса', ''),
            flight.get('тип самолета', '')
        ))

    click.echo(line)

def search_flights_by_aircraft_type(flights_list, search_aircraft_type):
    matching_flights = [flight for flight in flights_list if flight['тип самолета'] == search_aircraft_type]

    if matching_flights:
        click.echo("\nРейсы, обслуживаемые самолетом типа {}: ".format(search_aircraft_type))
        print_flights(matching_flights)
    else:
        click.echo(f"\nРейсов, обслуживаемых самолетом типа {search_aircraft_type}, не найдено.")

def save_to_json(filename, data):
    with open(filename, 'w', encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_from_json(filename):
    try:
        with open(filename, 'r', encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

@click.command()
@click.option('--add-flight', is_flag=True, help='Add a new flight')
@click.option('--print-flights', is_flag=True, help='Print the list of flights')
@click.option('--search-by-type', help='Search flights by aircraft type')
@click.option('--file', default='flights.json', help='JSON file to load/save flight data')
def main(add_flight, print_flights, search_by_type, file):
    if add_flight:
        destination = click.prompt('Введите название пункта назначения', type=str)
        flight_number = click.prompt('Введите номер рейса', type=str)
        aircraft_type = click.prompt('Введите тип самолета', type=str)
        flights_list = load_from_json(file)
        flights_list = add_flight(destination, flight_number, aircraft_type, flights_list)
        save_to_json(file, flights_list)

    elif print_flights:
        flights_list = load_from_json(file)
        print_flights(flights_list)

    elif search_by_type:
        flights_list = load_from_json(file)
        search_flights_by_aircraft_type(flights_list, search_by_type)

    else:
        click.echo("Пожалуйста, выберите действие из списка: --add-flight, --print-flights, or --search-by-type")

if __name__ == '__main__':
    main()
