from experta import Fact, Rule, KnowledgeEngine, L

class Light(Fact):
    """Info about the traffic light."""
    pass

class RobotCrossStreet(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.response = None

    @Rule(Light(color='green'))
    def green_light(self):
        self.response =  "Walk"

    @Rule(Light(color='red'))
    def red_light(self):
        self.response = "Don't walk"

    @Rule('light' << Light(color=L('yellow') | L('blinking-yellow')))
    def cautious(self, light):
        self.response = f"Be cautious because light is {light['color']}"

# Instantiate the system
system = RobotCrossStreet()

# Feed the facts to the system and run it
