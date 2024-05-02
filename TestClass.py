class TestClass:
    def __init__(self, x, y, string):
        self.x = x
        self.y = y
        self.string = string

    def add(self):
        return self.x + self.y

    def subtract(self):
        return self.x - self.y

    def divide(self, x):
        if self.y != 0:
            return self.x / self.y
        else:
            return "Cannot divide by zero"
    
    def concat_strings(self, s):
        return self.string + s
    
    def count_characters(self):
        return len(self.string)