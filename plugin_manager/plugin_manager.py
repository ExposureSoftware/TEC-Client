import json
import logging
import os
import sys
import traceback
from os.path import join, dirname, realpath
from appdirs import AppDirs

__author__ = 'pat'


class PluginManager:
    top_level = dirname(realpath(dirname(__file__)))
    if "zip" in top_level:
        top_level = realpath(dirname(top_level))
    path = join(top_level, 'plugins')
    try:
        if sys.frozen is True:
            dirs = AppDirs('Centurion Client', 'Exposure Software')
            config = dirs.user_config_dir + "\\plugin_config.json"
        else:
            config = join(path, 'plugin_config.json')
    except AttributeError:
        config = join(path, 'plugin_config.json')

    def __init__(self, send_command, echo):
        self.log = logging.getLogger(__name__)
        self.send_command = send_command
        self.echo = echo

        self.setup()

    def setup(self):
        self.plugins = {}
        self.plugin_enabled = {}
        self.pre_process_plugins = []
        self.post_process_plugins = []
        self.ui_plugins = []
        self.create_status_api()
        data = open(self.config, 'r').read()
        if data:
            self.plugin_enabled = json.loads(data)

        for root, dirs, files in os.walk(self.path, topdown=True):
            for d in dirs:
                if "__" not in d and "test" not in d and "pyglet" not in d:
                    self.find_plugins(join(self.path, d))
        self.save_plugin_config()

    def find_plugins(self, current_path):
        sys.path.insert(0, current_path)
        for root, dirs, files in os.walk(current_path, topdown=True):
            dirs[:] = [dir for dir in dirs if "__" not in dir and "test" not in dir and "pyglet" not in dir]
            for name in files:
                if name.endswith("_plugin.py"):
                    name = name.strip(".py")
                    try:
                        mod = __import__(name)
                        if hasattr(mod, "Plugin"):
                            self.plugins[name] = mod.Plugin()
                            if name not in self.plugin_enabled:
                                self.plugin_enabled[name] = True
                            self.register_apis(name, self.plugins[name])
                    except Exception as e:
                        self.log.error(traceback.format_exc())
        sys.path.pop(0)

    def register_apis(self, name, mod):
        if hasattr(mod, "set_send_command"):
            mod.set_send_command(self.send_command)
        if hasattr(mod, "set_echo"):
            mod.set_echo(self.echo)

        if hasattr(mod, "pre_process"):
            self.pre_process_plugins.append(name)
        if hasattr(mod, "post_process"):
            self.post_process_plugins.append(name)
        if hasattr(mod, "draw"):
            self.ui_plugins.append(name)
        if hasattr(mod, "health_update"):
            self.status_plugins['Health'].append(name)
        if hasattr(mod, "fatigue_update"):
            self.status_plugins['Fatigue'].append(name)
        if hasattr(mod, "encumbrance_update"):
            self.status_plugins['Encumbrance'].append(name)
        if hasattr(mod, "satiation_update"):
            self.status_plugins['Satiation'].append(name)

    def get_plugins(self):
        return self.plugins

    def save_plugin_config(self):
        config = open(self.config, 'w')
        try:
            config.write(json.dumps(self.plugin_enabled, indent=4, sort_keys=True))
        finally:
            config.close()

    def toggle_plugin(self, name, is_enabled):
        self.plugin_enabled[name] = is_enabled
        self.save_plugin_config()

    ### Line Processing
    def pre_process(self, line, tags):
        for name in self.pre_process_plugins:
            if self.plugin_enabled[name]:
                try:
                    self.plugins[name].pre_process(line)
                except Exception:
                    self.log.error(name + " Failure")
                    self.log.error(traceback.format_exc())

        # Maybe we do something like AND the result of all the process calls?
        # if any of them return that they handled it and we should not draw?
        return False

    def post_process(self, line, tags):
        for name in self.post_process_plugins:
            if self.plugin_enabled[name]:
                try:
                    self.plugins[name].post_process(line)
                except Exception:
                    self.log.error(name + " Failure")
                    self.log.error(traceback.format_exc())

    ### Plugin UI Handling
    def create_plugin_area(self, plugin_area):
        for name in self.ui_plugins:
            if self.plugin_enabled[name]:
                try:
                    self.plugins[name].draw(plugin_area)
                except Exception:
                    self.log.error(name + " Failure")
                    self.log.error(traceback.format_exc())

    ### Status Update API
    def create_status_api(self):
        self.status_plugins = {'Health': [], 'Fatigue': [], 'Encumbrance': [], 'Satiation': []}
        self.status_plugins_api_names = {'Health': 'health_update', 'Fatigue': 'fatigue_update',
                                         'Encumbrance': 'encumbrance_update', 'Satiation': 'satiation_update'}

    def status_update(self, status, value):
        for name in self.status_plugins[status]:
            if self.plugin_enabled[name]:
                try:
                    update_method = getattr(self.plugins[name], self.status_plugins_api_names[status])
                    update_method(value)
                except Exception:
                    self.log.error(name + " Failure")
                    self.log.error(traceback.format_exc())
