import yaml

def load_simulation_values(path):
    with open(path, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print("Got exception:", exc, "\nwhile parsing",path)
            exit()