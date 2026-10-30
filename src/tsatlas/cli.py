"""Command-line entry points; no network access during study execution."""
import argparse
import json
from .data import fetch, intake, verify_snapshots


def main():
    parser = argparse.ArgumentParser()
    studies=['co2','electricity','synthetic','retail','oil','river-flow','air-quality','ecg','spectral']
    parser.add_argument('command', choices=['fetch','intake','verify','all']+studies)
    parser.add_argument('study',nargs='?',choices=['retail','oil','river-flow','air-quality','ecg'])
    args = parser.parse_args()
    if args.command == 'fetch':
        if args.study:
            from .acquire import fetch_study
            print(json.dumps(fetch_study(args.study),indent=2))
        else:fetch()
    elif args.command == 'intake':
        if args.study:
            from .extended_data import retail_intake,oil_intake,air_quality_intake
            from .camels_source import intake as river_intake
            from .ecg_source import intake as ecg_intake
            fn={'retail':retail_intake,'oil':oil_intake,'air-quality':air_quality_intake,'river-flow':river_intake,'ecg':ecg_intake}[args.study]
            print(json.dumps(fn(),indent=2))
        else:print(json.dumps(intake(), indent=2))
    elif args.command in studies+['all']:
        from threadpoolctl import threadpool_limits
        import importlib
        studies=studies if args.command=='all' else [args.command]
        with threadpool_limits(limits=1):
            for study in studies:
                importlib.import_module('tsatlas.'+study.replace('-','_')).run()
    else:
        evidence=verify_snapshots()
        print('Present pinned analysis snapshots verified')
        if evidence['not_mirrored']:
            print('Fetch-only inputs absent and NOT verified: '+', '.join(evidence['not_mirrored']))
            print('Acquire oil input explicitly with: uv run atlas fetch oil')

if __name__ == '__main__':
    main()
