""" Command line interface to the application

Dynamically loads classes in view/cli/*.py that inherit views
"""
import glob
import importlib
import inspect
import logging
import os
import sys
from typing import List

import src.view.cli_view


def main(argv):
    """ Script's main function """
    cli_view_path = os.path.join('src', 'view', 'cli', '*.py')
    cli_view_objects = load_views(cli_view_path)

    # Build lookup class of view names to view objects
    view_lookup = {
        view.get_cli_name().lower(): view
        for view in cli_view_objects
    }
    # The "help" view is special in that in needs access to other views
    help_view = view_lookup['help']
    help_view.views = cli_view_objects
    if len(argv) == 1:
        print('Usage: %s <command> [<arg>, <arg>, ...]' % sys.argv[0])
        help_view.do_command([])

    elif len(argv) > 1:
        command_name = argv[1].lower()
        command_args = argv[2:]
        if command_name in view_lookup:
            view_lookup[command_name].do_command(command_args)

        else:
            print('Error, "%s" is not a recognized command' % command_name)


def load_views(path_name: str) -> List[src.view.cli_view.CliView]:
    """ Loads cli views in a given path """
    views = []

    logger.info('Searching view modules in path "%s"' % path_name)
    for python_file in glob.glob(path_name):
        module_name = script_name_to_module(python_file)
        logger.info('Loading module "%s"' % module_name)
        module = importlib.import_module(module_name)

        for attr_name in dir(module):
            if attr_name[0] == '_':
                # Skip anything starting with underscore
                continue

            module_attr = getattr(module, attr_name)
            if not inspect.isclass(module_attr):
                # Skip anything that isn't a class
                continue

            try:
                if issubclass(module_attr, src.view.cli_view.CliView):
                    logger.info(
                        'Loading class: "%s.%s"' % (module_name, attr_name)
                    )
                    views.append(module_attr())

            except TypeError as ex:
                logger.error('Bad attribute: %s' % attr_name)
                raise ex

    return views


def script_name_to_module(file_name: str) -> str:
    """ Converts python file name to importable module name """
    if file_name[-3:] != '.py':
        raise ValueError('Script name "%s" should end in ".py' % file_name)
    parts = file_name[:-3].split(os.path.sep)
    return '.'.join(parts)


# Setup logger
logging.basicConfig(level=logging.INFO, filename='data/cli.log')
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    main(sys.argv)
