from argparse import ArgumentParser, FileType

nest_parser = ArgumentParser(description='Nest a flat dictionaries')
nest_parser.add_argument(
    'keys', type=str, nargs='+',
    help='keys for grouping',
)
nest_parser.add_argument(
    'json', type=FileType('r'), default='-', nargs='?',
    help='json data to process',
)
nest_parser.add_argument(
    '-i', '--indent', type=int, default=4,
    help='indentation for printing output result',
)
