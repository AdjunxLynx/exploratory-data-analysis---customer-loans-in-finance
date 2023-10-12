import yaml


class RDSDatabaseConnector():
    def init():
        pass

    def load_credentials():
            with open('credentials.yaml', 'r') as file:
                credentials = yaml.load(file)
            return credentials