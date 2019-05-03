import yaml

def before_all(context):
    config = open('config.yaml', 'r')
    context.config = yaml.safe_load(config)
