class Plugin:

    def __init__(self):
        print("look plugin init")

    def post_process(self, line, send_command, echo):
        if line.strip() == "look":
            echo("You looked!")