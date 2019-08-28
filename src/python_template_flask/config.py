import os
import pathlib

import dataset
import yaml


def config_directories():
    """Directories to look for config.

    Return:
        list: A list of possible config directories
    """
    dirs = [
        '.',
        '~/.config/python_template_flask/',
        '/etc/python_template_flask',
    ]
    return dirs


def config_files():
    """Location is all config files.

    Return:
        list: A list of config file paths
    """
    filename = 'settings.yaml'

    files = []
    for cdir in config_directories():
        path = pathlib.Path(cdir).expanduser().absolute()
        files.append(path / filename)
    return files


def find_config():
    """Find the application config.

    Return:
        dict: All environments as keys with flask options
    """
    settings = {}
    for config in config_files():
        if config.is_file():
            settings = yaml.safe_load(config.read_text())
            break
    return settings


def get_config():
    """Get configuration data.

    Return:
        dict: Environment with flask options
    """
    config = find_config()
    env = os.environ.get('FLASK_ENV', 'production')
    return config.get(env, {})


def get_database(app_config):
    """Get database object.

    Return:
        dataset.database.Database: Connected database object
    """
    db_config = app_config.get('DB')
    if db_config is None:
        db_config = {}

    db_port = os.environ.get('POSTGRES_5432_TCP', '5432')
    db_uri_raw = os.environ.get('DATABASE_URL') or db_config.get('URI', 'sqlite:///:memory:')
    db_uri = db_uri_raw.replace('$PORT', db_port)
    db_info = {
        'url': db_uri,
        'engine_kwargs': db_config.get('OPTIONS', None),
    }
    return dataset.connect(**db_info)


def get_plugin_paths(resource):
    app_config = get_config()
    plugin_resources = app_config.get('extra_plugins', {})
    extra_plugins = plugin_resources.get(resource, [])
    return extra_plugins


APP_CONFIG = get_config()
DATABASE = get_database(APP_CONFIG)
