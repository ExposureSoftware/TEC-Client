import os
import sys

__author__ = 'pat'


class PluginManager():
    path = "plugin_manager/plugins"

    def __init__(self):
        self.plugins = {}
        self.plugin_status = {}

        self.create_status_api()

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
                        if hasattr(mod, "health_update"):
                            self.status_plugins['Health'].append(name)
                        if hasattr(mod, "fatigue_update"):
                            self.status_plugins['Fatigue'].append(name)
                        if hasattr(mod, "encumbrance_update"):
                            self.status_plugins['Encumbrance'].append(name)
                        if hasattr(mod, "satiation_update"):
                            self.status_plugins['Satiation'].append(name)
                    except Exception as e:
                        pass
            for name in dirs:
                self.find_plugins(current_path + "/" + name)

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

    # Status Update API
    def create_status_api(self):
        self.status_plugins = {}
        self.status_plugins['Health'] = []
        self.status_plugins['Fatigue'] = []
        self.status_plugins['Encumbrance'] = []
        self.status_plugins['Satiation'] = []
        self.status_plugins_api_names = {}
        self.status_plugins_api_names['Health'] = 'health_update'
        self.status_plugins_api_names['Fatigue'] = 'fatigue_update'
        self.status_plugins_api_names['Encumbrance'] = 'encumbrance_update'
        self.status_plugins_api_names['Satiation'] = 'satiation_update'

    def status_update(self, status, value):
        for plugin in self.status_plugins[status]:
            if self.plugin_status[plugin]:
                update_method = getattr(self.plugins[plugin], self.status_plugins_api_names[status])
                update_method(value)
