class Plugin:
    def __init__(self):
        print("Look Plugin: init")

    def process(self, line, send_command):
        if "look" in line:
            print("You looked!")

    def draw(self, plugin_area):
        pass