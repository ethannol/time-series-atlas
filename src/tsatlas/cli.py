"""Command-line entry points; no network access during study execution."""
import argparse
import json
from .data import fetch, intake, verify_snapshots


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['fetch','intake','verify'])
    args = parser.parse_args()
    if args.command == 'fetch':
        fetch()
    elif args.command == 'intake':
        print(json.dumps(intake(), indent=2))
    else:
        verify_snapshots()
        print('Pinned analysis snapshots verified')

if __name__ == '__main__':
    main()
