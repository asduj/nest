import json
import sys
from abc import ABC, abstractmethod
from io import StringIO
from json import JSONDecodeError
from typing import Any, List

from .exceptions import InputFormatError


__all__ = [
    'SanitisePresenter',
    'ConsoleSanitisePresenter',
    'SanitiseUseCase',
]


class SanitisePresenter(ABC):  # pragma: no cover
    @abstractmethod
    def invalid_json(self, details=None) -> Any:
        return 'The input data is not a valid JSON'

    @abstractmethod
    def wrong_format(self, details=None) -> Any:
        return 'Input data should be flat list (array) of dictionaries (objects)'


class ConsoleSanitisePresenter(SanitisePresenter):  # pragma: no cover
    def __init__(self, err_stream: StringIO = sys.stderr) -> None:
        self.err_stream = err_stream

    def err_print(self, *args, **kwargs) -> None:
        print(*args, file=self.err_stream, **kwargs)
        exit(-1)

    def invalid_json(self, details=None) -> None:
        self.err_print(super().invalid_json())
        if details:
            self.err_print(details)

    def wrong_format(self, details=None) -> None:
        if details is not None:
            return self.err_print(details)

        self.err_print(super().wrong_format())


class SanitiseUseCase:
    def __init__(self, presenter: SanitisePresenter, file: StringIO) -> None:
        self.presenter = presenter
        self.file = file

    def process_data(self) -> List[dict]:
        try:
            return self._sanity_json()
        except JSONDecodeError as exc:
            return self.presenter.invalid_json(f'{exc}\nGot: {exc.doc}')
        except InputFormatError:
            return self.presenter.wrong_format()

    def _sanity_json(self) -> List[dict]:
        raw_input = ''.join(self.file.readlines())
        json_data = json.loads(raw_input)
        if not isinstance(json_data, list):
            raise InputFormatError
        return json_data
