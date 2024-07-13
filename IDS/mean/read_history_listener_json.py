import json


class Read_history_listener_json:

    def __init__(self):
        with open('../history/listener_history.json', 'r', encoding='utf-8') as json_file:
            self.data = json.load(json_file)

    def get_history_list(self):
        name = []
        interface = []
        time = []

        for history in self.data['history']:
            name.append(history['name'])
            interface.append(history['interface'])
            time.append(history['last_open_time'])

        return name, interface, time
