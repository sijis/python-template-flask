"""Manager to handle plugins"""
import pathlib

from pluginbase import PluginBase


class PluginManager:
    """Manage plugins

    Args:
        resource (str): Path of plugin directory.
        name (str): The name of the plugin.
    """

    def __init__(self, resource, name):
        path = pathlib.Path(__file__).parent.resolve()
        path = path / resource

        all_paths = [str(path)]

        self.paths = all_paths
        self.name = name

        plugin_base = PluginBase(package='python_template_flask.plugins')
        self.plugin_source = plugin_base.make_plugin_source(searchpath=self.paths, persist=True)

    def plugins(self):
        """List of all plugins available."""
        for plugin in self.plugin_source.list_plugins():
            yield plugin

    def load(self):
        """Load the plugin."""
        loaded_plugin = self.plugin_source.load_plugin(self.name)
        return loaded_plugin


def get_plugin(plugin_dir, plugin_name):
    """Wrapper around PluginManager"""
    manager = PluginManager(plugin_dir, plugin_name)
    plugin = manager.load()
    return plugin


def get_plugins(plugin_dir, prefix):
    manager = PluginManager(plugin_dir, '')
    available_plugins = manager.plugins()
    for plugin in available_plugins:
        if plugin.startswith(prefix):
            yield plugin
