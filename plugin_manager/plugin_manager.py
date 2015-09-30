import os
import sys

__author__ = 'pat'


class PluginManager():
    path = "plugin_manager/plugins"
    plugins = {}

    def __init__(self, send_command):
        self.find_plugins(self.path, send_command)
        print(self.plugins)

    def find_plugins(self, current_path, send_command):
        sys.path.insert(0, current_path)
        for root, dirs, files in os.walk(current_path, topdown=True):
            for name in files:
                if name.endswith(".py"):
                    print(os.path.join(root, name))
                    name = name.strip(".py")
                    # if ext == '.py':
                    try:
                        mod = __import__(name)
                        self.plugins[name] = mod.Plugin(send_command)
                    except Exception as e:
                        print(e.__doc__)
            for name in dirs:
                self.find_plugins(current_path + "/" + name, send_command)
        sys.path.pop(0)

    def pre_draw_plugins(self, line, tags):
        for plugin in self.plugins.values():
            plugin.process(line)

    def post_draw_plugin(self, line, tags):
        pass

    def create_plugin_area(self, plugin_area):
        for plugin in self.plugins.values():
            plugin.draw(plugin_area)
