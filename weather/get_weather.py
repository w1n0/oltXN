from pyowm import OWM
from pyowm.utils.config import get_default_config

config_dict = get_default_config()
config_dict['language'] = 'ru'
owm = OWM('e6910af1fedcad1885a807ec3a1b3a6f', config_dict)
mgr = owm.weather_manager()


def getting_temperature(city):
    observation = mgr.weather_at_place(city)
    w = observation.weather
    return int(w.temperature('celsius')['temp'])


def getting_wind(city):
    observation = mgr.weather_at_place(city)
    w = observation.weather
    return w.wind()['speed']


def getting_humidity(city):
    observation = mgr.weather_at_place(city)
    w = observation.weather
    return w.humidity


def getting_status(city):
    observation = mgr.weather_at_place(city)
    w = observation.weather
    return w.detailed_status