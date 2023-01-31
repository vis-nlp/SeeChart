import csv


class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'


users = []


with open('static/users/users.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    for a in csv_reader:
        users.append(User(id=str(a["id"]), username=str(a["username"]), password="password"+str(a["password"])))

