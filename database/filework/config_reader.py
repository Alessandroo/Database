import configparser
import os


def get_config_parameter(parameter, project='DEFAULT'):
    old_directory = os.getcwd()
    os.chdir("../")
    config = configparser.ConfigParser()
    config.read('database.ini')
    data = config[project][parameter]
    os.chdir(old_directory)
    return data


def print_parameters(project='Default'):
    config = configparser.ConfigParser()
    config.read('database.ini')
    for key in config[project]:
        print(key)


if __name__ == '__main__':
    print(get_config_parameter("path"))
