"""Command-line entry points; no network access during study execution."""
import argparse
import json
from .data import fetch, intake, verify_snapshots


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['fetch','intake','verify','co2','electricity','synthetic','all'])
    args = parser.parse_args()
    if args.command == 'fetch':
        fetch()
    elif args.command == 'intake':
        print(json.dumps(intake(), indent=2))
    elif args.command in ['co2','electricity','synthetic','all']:
        from threadpoolctl import threadpool_limits
        import importlib
        studies=['co2','electricity','synthetic'] if args.command=='all' else [args.command]
        with threadpool_limits(limits=1):
            for study in studies:
                importlib.import_module('tsatlas.'+study).run()
    else:
        verify_snapshots()
        print('Pinned analysis snapshots verified')

if __name__ == '__main__':
    main()
