class Plugin:
    def __init__(self):
        print("Look Plugin: init")

    def process(self, line):
        if "look" in line:
            print("You looked!")
