import argparse
import importlib
import os
import pkgutil
import spexxy.tools
import logging


def main():
    # init logging
    logging.basicConfig(format='[%(asctime)s] %(message)s', level=logging.INFO)
    logging.captureWarnings(True)

    # init parser
    parser = argparse.ArgumentParser(description='spexxy command line interface',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    subparsers = parser.add_subparsers(help='sub-command help')

    # list modules in spexxy.methods
    pkgpath = os.path.dirname(spexxy.tools.__file__)
    modules = [name for _, name, _ in pkgutil.iter_modules([pkgpath])]

    # loop modules
    for m in modules:
        # import module
        mod = importlib.import_module('spexxy.tools.' + m)
        # add subparser
        try:
            mod.add_parser(subparsers)
        except AttributeError:
            continue

    # parse arguments
    args = parser.parse_args()

    # and call method
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()


