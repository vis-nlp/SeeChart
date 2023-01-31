import json
import datetime
import os.path


class Tasks(object):
    data = {
        'last_updated': None,
        'pid': None,
        'logged_in': None
    }

    fileName: str

    def __init__(self, pid):
        self.pid = pid
        self.fileName = 'data_' + pid

        if os.path.isfile('static/task/' + self.fileName + '.json'):
            print(self.fileName + '.json already exists!')
            f = open('static/task/' + self.fileName + '.json')
            found_data = json.load(f)
            self.data = found_data
            self.update_task_list()

        else:
            f = open('static/task/checklist.json')
            checklist = json.load(f)
            for a in checklist:
                self.data[checklist[a]] = "NOT DONE"

            # print(checklist)

            self.data['pid'] = str(pid)
            self.data['last_updated'] = str(datetime.datetime.now())
            self.set_logged_in_true()

            self.update_json()

    def set_task_status(self, task_name, status):
        if task_name in self.data:
            self.data[task_name] = status
            self.data['last_updated'] = str(datetime.datetime.now())
            self.update_json()
        else:
            raise Exception("TASK NAME WAS NOT FOUND IN " + self.fileName + ".json!")

    def set_logged_in_true(self):
        if 'logged_in' in self.data:
            self.data['logged_in'] = 'true'
            self.update_json()
        else:
            raise Exception("TASK NAME WAS NOT FOUND IN " + self.fileName + ".json!")

    def set_logged_in_false(self):
        if 'logged_in' in self.data:
            self.data['logged_in'] = 'false'
            self.update_json()
        else:
            raise Exception("TASK NAME WAS NOT FOUND IN " + self.fileName + ".json!")

    def get_logged_in_status(self):
        if 'logged_in' in self.data:
            return self.data['logged_in']
        else:
            raise Exception("TASK NAME WAS NOT FOUND IN " + self.fileName + ".json!")

    def get_task_status(self, task_name):
        if task_name in self.data:
            return self.data[task_name]
        else:
            raise Exception("TASK NAME WAS NOT FOUND IN " + self.fileName + ".json!")

    def get_all_task_status_info(self):
        return self.data

    def update_json(self):
        with open('static/task/' + self.fileName + '.json', 'w') as f:
            json.dump(self.data, f, indent=4)
        print(self.fileName + ".json updated")

    def update_task_list(self):
        f = open('static/task/checklist.json')
        checklist = json.load(f)
        changed = 0
        for a in checklist:
            if checklist[a] not in self.data:
                changed = 1
                self.data[checklist[a]] = "NOT DONE"

        to_be_popped = []

        for a in self.data:
            if a == "last_updated" or a == "pid" or a == "logged_in":
                pass
            elif a not in checklist.values():
                print('THIS DID NOT MATCH: ')
                print(a)
                to_be_popped.append(a)
                changed = 1

        for a in to_be_popped:
            self.data.pop(a, None)

        if changed == 1:
            self.update_json()
            print("Updated!")
            return True
        else:
            print("No changes found in checklist.json!")
            return False

    def reset_data(self):
        for a in self.data:
            if a == "last_updated" or a == "pid":
                pass
            else:
                self.data[a] = "NOT DONE"
        self.update_json()


# t = tasks('123')
# d = t.get_all_task_status_info()
#
# print(json.dumps(d, indent=4))
#
# t.set_task_status('TASK C', 'DONE')
#
# if t.update_task_list():
#     d = t.get_all_task_status_info()
#     print(json.dumps(d, indent=4))
#
# t.reset_data()