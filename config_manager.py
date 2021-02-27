import json


class ConfigManager():
    def __init__(self):
        self.transaction_dir = None
        self.blocks_dir = None
        self.private_key_path = None
        self.public_key_path = None

    def to_json(self):
        dict = {
            'transaction': self.transaction_dir,
            'blocks_dir': self.blocks_dir,
            'private_key_path': self.private_key_path,
            'public_key_path': self.public_key_path
        }
        return dict

    def dump(self, file_path):
        with open(file_path, 'w') as file_json:
            json.dump(self.to_json(), file_json, indent = 4)

    def from_json(self, json_file_path):
        with open(json_file_path, 'r') as json_file:
            json_dict = json.loads(json_file.read())

        self.transaction_dir = json_dict['transaction_dir']
        self.block_dir = json_dict['blocks_dir']
        self.private_key_path = json_dict['private_key_path']
        self.public_key_path = json_dict['public_key_path']

    def __str__(self):
        return str(self.to_json())
