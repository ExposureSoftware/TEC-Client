import os
import sys

__author__ = 'pat'


class PluginManager():
    path = "plugin_manager/plugins"

    def __init__(self):
        self.plugins = {}
        self.plugin_status = {}
        self.find_plugins(self.path)

    def find_plugins(self, current_path):
        sys.path.insert(0, current_path)
        for root, dirs, files in os.walk(current_path, topdown=True):
            for name in files:
                if name.endswith(".py"):
                    name = name.strip(".py")
                    try:
                        mod = __import__(name)
                        self.plugins[name] = mod.Plugin()
                        self.plugin_status[name] = True
                    except Exception as e:
                        pass
            for name in dirs:
                self.find_plugins(current_path + "/" + name)
        sys.path.pop(0)

    def pre_draw_plugins(self, line, tags, send_command):
        for key, plugin in self.plugins.items():
            if self.plugin_status[key]:
                plugin.process(line, send_command)

        # Maybe we do something like AND the result of all the process calls? if any of them return that they handled it and we should not draw
        return False

    def post_draw_plugin(self, line, tags):
        pass

    def create_plugin_area(self, plugin_area):
        for key, plugin in self.plugins.items():
            if self.plugin_status[key]:
                plugin.draw(plugin_area)

    def get_plugins(self):
        return self.plugins

    def toggle_plugin(self, name, is_enabled):
        self.plugin_status[name] = is_enabled
