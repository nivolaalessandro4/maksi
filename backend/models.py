class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def save_to_database(self):
        # Code to save user data to database
        pass

    @classmethod
    def from_json(cls, json_data):
        # Code to create User object from JSON data
        name = json_data['name']
        email = json_data['email']
        return cls(name, email)
