import json
import sys


def load_bars_data(bars_data_filepath):
    data_filepath = bars_data_filepath
    while True:
        try:
            with open(data_filepath, encoding='utf-8') as data_file:
                return json.loads(data_file.read())
        except FileNotFoundError:
            data_filepath = input(
                    'Файл не найден, напиши правильный путь к файлу:')
        except json.decoder.JSONDecodeError:
            data_filepath = input(
                    'Файл не содержит JSON, напиши правильный путь к файлу:')


def coordinates_input(input_question):
    while True:
        try:
            return float(input(input_question))
        except ValueError:
            print('Не балуйся, введи координаты в числовом виде!')


def get_biggest_bars(bars_data):
    biggest_bars = []
    max_bar_seats = max(bar['SeatsCount'] for bar in bars_data)
    for bar in bars_data:
        if bar['SeatsCount'] == max_bar_seats:
            biggest_bars.append(bar)
    return biggest_bars


def get_smallest_bars(bars_data):
    smallest_bars = []
    min_bar_seats = min(bar['SeatsCount'] for bar in bars_data)
    for bar in bars_data:
        if bar['SeatsCount'] == min_bar_seats:
            smallest_bars.append(bar)
    return smallest_bars


def get_closest_bar(bars_data, user_longitude, user_latitude):
    return min(bars_data, key=lambda bar:
               (bar['geoData']['coordinates'][1] - user_latitude) ** 2 +
               (bar['geoData']['coordinates'][0] - user_longitude) ** 2)


def print_bar_info(description, bar_data):
    print('{}: {}, посадочных мест:{}, находится по адресу: {}'.format(
           description, bar_data['Name'], bar_data['SeatsCount'],
           bar_data['Address']))


if __name__ == '__main__':
    bars_data_filepath = sys.argv[1]
    bars_data = load_bars_data(bars_data_filepath)
    biggest_bars = get_biggest_bars(bars_data)
    smallest_bars = get_smallest_bars(bars_data)
    for bar in biggest_bars:
        print_bar_info('самый большой бар', bar)
    for bar in smallest_bars:
        print_bar_info('самый маленький бар', bar)
    print('А теперь давай узнаем, какой бар ближе. Введи свои координаты.')
    user_latitude = coordinates_input(
            'Узнай в гугле, на какой широте ты находишься:')
    user_longitude = coordinates_input(
            'Отлично, теперь узнай в гугле, на какой долготе ты находишься:')
    nearest_bar = get_closest_bar(bars_data, user_longitude, user_latitude)
    print_bar_info('ближайший бар', bar)
