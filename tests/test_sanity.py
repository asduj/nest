from unittest.mock import MagicMock
from nest.sanity import SanitisePresenter, SanitiseUseCase
from pathlib import Path
from io import StringIO


presenter = MagicMock(spec_set=SanitisePresenter, **{
    'wrong_format.return_value': None,
    'invalid_json.return_value': None,
})


def test_sanitise_use_case__ok():
    presenter.reset_mock()
    file = Path(__file__).parent / 'fixtures' / 'input.json'

    use_case = SanitiseUseCase(presenter, file.open())
    result = use_case.process_data()

    assert result
    assert isinstance(result, list)
    assert isinstance(result[0], dict)


def test_sanitise_use_case__input_data_not_list():
    presenter.reset_mock()
    file = StringIO('{}')

    use_case = SanitiseUseCase(presenter, file)

    assert not use_case.process_data()
    assert presenter.wrong_format.called


def test_sanitise_use_case__invalid_json():
    presenter.reset_mock()
    file = StringIO("{'key': 'value'}")

    use_case = SanitiseUseCase(presenter, file)

    assert not use_case.process_data()
    assert presenter.invalid_json.called
