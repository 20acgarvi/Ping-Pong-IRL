
class Console:
    def __init__(self, *args, **kwargs):
        self.activated = true
        #keywords is a dict containing all valid commands
        if "keywords" in kwargs:
            self.keywords = keywords

    def activate(self):
        self.activated = true
    
    
