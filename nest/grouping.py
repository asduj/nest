import json
import sys
from abc import ABC, abstractmethod
from copy import deepcopy
from functools import partial
from io import StringIO
from itertools import groupby
from operator import itemgetter, delitem
from typing import Any, List, Tuple, Union

from nest.exceptions import CompositeValueError, LimitedKeysNumberError

__all__ = [
    'GroupingPresenter',
    'GroupingConsolePresenter',
    'GroupingUseCase',
]


class GroupingPresenter(ABC):  # pragma: no cover
    @abstractmethod
    def show_result(self, data: dict) -> Any:
        pass

    @abstractmethod
    def key_is_not_exist(self, key: str) -> Any:
        return f'Specified key "{key}" is not exist in input JSON data'

    @abstractmethod
    def limited_keys_number(self, data: dict, keys: Tuple[str, ...]) -> Any:
        message = (
            'Dictionary (object) should at least contains on 1 key more '
            'then level of nesting. Nesting level is {0}, number of keys is {1}'
        )

        return message.format(len(keys), len(data.keys()))

    @abstractmethod
    def composite_value_is_forbidden(self, data: Any) -> Any:
        return f'Expected simple value like string or number, got {type(data)}.'


class GroupingConsolePresenter(GroupingPresenter):  # pragma: no cover
    def __init__(self, indent: int = 4, err_stream: StringIO = sys.stderr) -> None:
        self.indent = indent
        self.err_stream = err_stream

    def err_print(self, *args, **kwargs) -> None:
        print(*args, file=self.err_stream, **kwargs)

    def show_result(self, data: dict) -> None:
        print(json.dumps(data, indent=self.indent))

    def key_is_not_exist(self, key: str) -> None:
        self.err_print(super().key_is_not_exist(key))

    def limited_keys_number(self, data: dict, keys: Tuple[str, ...]) -> Any:
        self.err_print(super().limited_keys_number(data, keys))

    def composite_value_is_forbidden(self, data: Any) -> None:
        self.err_print(super().composite_value_is_forbidden(data))


class GroupingUseCase:
    def __init__(
            self,
            presenter: GroupingPresenter,
            data: List[dict],
    ) -> None:
        self.data = data
        self.presenter = presenter

    def group_by(self, *items: str) -> dict:
        try:
            sorted_data = sorted(self.data, key=itemgetter(*items))
            return self.presenter.show_result(
                self._grouper(sorted_data, items, drop=items)
            )
        except KeyError as exc:
            return self.presenter.key_is_not_exist(exc.args[0])
        except CompositeValueError as exc:
            return self.presenter.composite_value_is_forbidden(exc.args[0])
        except LimitedKeysNumberError as exc:
            return self.presenter.limited_keys_number(exc.args[0], items)

    def _grouper(
            self,
            data: List[dict],
            items: Tuple[str, ...],
            drop: Tuple[str, ...],
    ) -> Union[dict, List[dict]]:
        if not items:
            # noinspection PyTypeChecker
            return list(map(partial(self._dropper, items=drop), data))

        result, item = {}, items[0]

        for key, group in groupby(data, itemgetter(item)):
            try:
                result[key] = self._grouper(list(group), items[1:], drop)
            except TypeError:
                raise CompositeValueError(key)

        return result

    @staticmethod
    def _dropper(data: dict, items: Tuple[str, ...]) -> dict:
        result = deepcopy(data)

        if len(result.keys()) <= len(items):
            raise LimitedKeysNumberError(result)
        # noinspection PyTypeChecker
        list(map(partial(delitem, result), items))

        return result
