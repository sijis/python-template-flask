from unittest import mock

from python_template_flask.config import config_directories, config_files, find_config


def test_config_directories():
    """Test 'config_directories()' function."""
    cdir = config_directories()
    assert list == type(cdir)


def test_config_files():
    """Test 'config_files()' function."""
    cfiles = config_files()
    for config in cfiles:
        assert config.name == 'settings.yaml'


@mock.patch('python_template_flask.config.config_files')
def test_find_config_nofile(config_file):
    """Test 'find_config()' function."""
    config_file.return_value = []
    config = find_config()
    assert config == {}


def test_find_config_hasfile():
    """Test 'find_config()' function."""
    config = find_config()
    assert config.get('production', False)
