import os

import appdirs  # type: ignore [import]
import click_config_file  # type: ignore [import]
import yaml


def yaml_config_option():
    path = os.path.join(appdirs.user_config_dir(appname=__package__), 'config.yaml')

    def provider(file_path, _cmd_name):
        if os.path.isfile(file_path):
            with open(file_path) as f:
                return yaml.safe_load(f)
        else:
            return {}

    return click_config_file.configuration_option(implicit=False, default=path, show_default=True, provider=provider)
