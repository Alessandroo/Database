import configparser


def get_config_parameter(parameter, project='DEFAULT'):
    print(parameter)
    config = configparser.ConfigParser()
    config.read('database.ini')
    return config[project][parameter]


def print_parameters(project='Default'):
    config = configparser.ConfigParser()
    config.read('database.ini')
    for key in config[project]:
        print(key)


if __name__ == '__main__':
    print(get_config_parameter("path"))
