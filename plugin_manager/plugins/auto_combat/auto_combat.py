from plugin_manager.plugins.auto_combat import Action


class Plugin:
    def __init__(self):
        print("AutoCombat: init")
        self.in_combat = False
        self.free = True

    def process(self, line):
        if self.in_combat:
            self.combat.handle_combat_line(line)
        elif "You are no longer busy" in line:
            print("Not Busy")
            self.free = True
            self.perform_action()
        elif ( "] A" in line or "] An" in line) and "You retrieve the line" not in line:
            print("Combat")
            self.in_combat = True
        elif "retreat" in line and "You retreat." not in line and "retreat first" not in line and "retreats." not in line:
            print("Retreating")
            self.add_action(Action.retreat)