import os
import sys

__author__ = 'pat'


class PluginManager:
    path = "plugin_manager/plugins"
    plugins = {}

    def __init__(self):
        sys.path.insert(0, self.path)
        for f in os.listdir(self.path):
            fname, ext = os.path.splitext(f)
            if ext == '.py':
                mod = __import__(fname)
                self.plugins[fname] = mod.Plugin()
        sys.path.pop(0)

    def pre_draw_plugins(self, line, tags):
        for plugin in self.plugins.values():
            plugin.process(line)

    def post_draw_plugin(self, line, tags):
        for plugin in self.plugins.values():
            plugin.process(line)

    def create_plugin_area(self, plugin_area):
        for plugin in self.plugins.values():
            plugin.draw(plugin_area)
