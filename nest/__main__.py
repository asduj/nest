from .grouping import GroupingUseCase, GroupingConsolePresenter
from .parser import nest_parser
from .sanity import SanitiseUseCase, ConsoleSanitisePresenter

args = nest_parser.parse_args()

data = SanitiseUseCase(
    presenter=ConsoleSanitisePresenter(),
    file=args.json,
).process_data()

GroupingUseCase(
    presenter=GroupingConsolePresenter(indent=args.indent),
    data=data,
).group_by(*args.keys)
