class Plugin:
    def __init__(self, send_command):
        print("Look Plugin: init")
        self.send_command = send_command

    def process(self, line):
        if "look" in line:
            print("You looked!")

    def draw(self, plugin_area):
        pass