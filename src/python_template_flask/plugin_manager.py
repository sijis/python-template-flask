"""Manager to handle plugins"""
import pathlib

from pluginbase import PluginBase


class PluginManager:
    """Manage plugins

    Args:
        resource (str): Path of plugin directory.
    """
    def __init__(self, resource, search_path=None):
        all_paths = []
        path = pathlib.Path(__file__).parent.resolve()
        path = path / resource
        all_paths.append(str(path))

        if search_path:
            all_paths.extend(search_path)

        self.paths = all_paths

        plugin_base = PluginBase(package='python_template_flask.plugins')
        self.plugin_source = plugin_base.make_plugin_source(searchpath=self.paths, persist=True)

    def plugins(self):
        """List of all plugins available."""
        for plugin in self.plugin_source.list_plugins():
            yield plugin

    def load(self, name):
        """Load the plugin.

        Args:
            name (str): The name of the plugin.
        """
        loaded_plugin = self.plugin_source.load_plugin(name)
        return loaded_plugin


def get_plugin(plugin_dir, plugin_name, extra_plugins=None):
    """Wrapper around PluginManager

    Args:
        plugin_dir (str): Path of plugin directory.
        name (str): The name of the plugin.
    """
    manager = PluginManager(resource=plugin_dir, search_path=extra_plugins)
    plugin = manager.load(plugin_name)
    return plugin


def get_plugins(plugin_dir, prefix=None, extra_plugins=None):
    """Get plugins starting with a prefix

    Args:
        plugin_dir (str): Path of plugin directory.
        prefix (str): Plugin prefix to match.
    """
    if not prefix:
        prefix = ''
    manager = PluginManager(resource=plugin_dir, search_path=extra_plugins)
    available_plugins = manager.plugins()
    for plugin in available_plugins:
        if plugin.startswith(prefix):
            yield plugin
