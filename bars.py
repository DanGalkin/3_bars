import json
import sys

def print_error(error):
    errors_dict = {
        'no_param': 'Ты не указал файл с данными при запуске программы.',
        'no_file': 'Такого файла нет, напиши правильный путь к файлу.',
        'no_json': 'В файле нет json, напиши путь к правильному файлу.',
        'not_number': 'Не балуйся, введи координаты в числовом виде!',
        'not_utf': 'Файл с данными не в utf, напиши путь к правильному файлу'
    }
    print(errors_dict[error])
    print('Программа автоматически завершит работу.')


def load_bars_data(filepath):
    with open(filepath, encoding='utf-8') as data_file:
        return json.loads(data_file.read())


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
    try:
        bars_data_file = sys.argv[1]
        bars_data = load_bars_data(bars_data_file)
    except IndexError:
        print_error('no_param')
        sys.exit()
    except FileNotFoundError:
        print_error('no_file')
        sys.exit()
    except UnicodeEncodeError:
        print_error('no_utf')
        sys.exit()
    except json.decoder.JSONDecodeError:
        print_error('no_json')
        sys.exit()
    biggest_bars = get_biggest_bars(bars_data)
    smallest_bars = get_smallest_bars(bars_data)
    for bar in biggest_bars:
        print_bar_info('Самый большой бар', bar)
    for bar in smallest_bars:
        print_bar_info('Самый маленький бар', bar)
    print('А теперь давай узнаем, какой бар ближе. Введи свои координаты.')
    try:
        user_latitude = float(input('Узнай в гугле, на какой '
                                    'широте ты находишься:'))
        user_longitude = float(input('Так, теперь узнай в гугле, на какой '
                                     'долготе ты находишься:'))
    except ValueError:
        print_error('not_number')
        sys.exit()
    nearest_bar = get_closest_bar(bars_data, user_longitude, user_latitude)
    print_bar_info('Ближайший бар', nearest_bar)
