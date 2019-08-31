import json
from pathlib import Path
from unittest.mock import MagicMock

from nest.grouping import GroupingUseCase, GroupingPresenter

fixtures = Path(__file__).parent / 'fixtures'

input_data = json.loads((fixtures / 'input.json').read_text())
output_data = json.loads((fixtures / 'output.json').read_text())

presenter = MagicMock(
    spec_set=GroupingPresenter,
    **{'show_result.side_effect': lambda data: data}
)
grouping_use_case = GroupingUseCase(presenter, input_data)


def test_grouping__ok():
    presenter.reset_mock()

    result = grouping_use_case.group_by('currency', 'country', 'city')

    assert result == output_data
    assert presenter.show_result.called


def test_grouping__key_not_exists():
    presenter.reset_mock()

    grouping_use_case.group_by('currency', 'country', 'capital')

    assert presenter.key_is_not_exist.called
    assert not presenter.show_result.called


def test_grouping__nesting_level_more_than_keys_number():
    presenter.reset_mock()

    grouping_use_case.group_by('currency', 'country', 'city', 'amount')

    assert presenter.limited_keys_number.called


def test_grouping__composite_value():
    presenter.reset_mock()
    input_data = [
        {
            'city': 'Minsk',
            'country': 'Belarus',
            'currency': 'USD',
            'amount': {
                'value': 100
            }
        }
    ]

    GroupingUseCase(presenter, input_data).group_by('amount')

    assert presenter.composite_value_is_forbidden.called
