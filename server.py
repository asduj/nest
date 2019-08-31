from typing import List, Any, Tuple, NoReturn

from fastapi import FastAPI, Query, Depends, HTTPException
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from starlette.responses import JSONResponse
from starlette.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from nest import (
    SanitisePresenter,
    GroupingUseCase, GroupingPresenter,

)

app = FastAPI()


class SanitiseJSONPresenter(SanitisePresenter):
    def invalid_json(self, details=None) -> NoReturn:
        raise NotImplementedError

    def wrong_format(self, details=None) -> JSONResponse:
        error = details or super().wrong_format()
        return JSONResponse(
            content={'error': error},
            status_code=HTTP_400_BAD_REQUEST,
        )


class GroupingJSONPresenter(GroupingPresenter):  # pragma: no cover
    def show_result(self, data: dict) -> JSONResponse:
        return JSONResponse(
            content=data,
            status_code=HTTP_200_OK,
        )

    def key_is_not_exist(self, key: str) -> JSONResponse:
        return JSONResponse(
            content=super().key_is_not_exist(key),
            status_code=HTTP_400_BAD_REQUEST,
        )

    def limited_keys_number(
            self,
            data: dict,
            keys: Tuple[str, ...],
    ) -> JSONResponse:
        return JSONResponse(
            content=super().limited_keys_number(data, keys),
            status_code=HTTP_400_BAD_REQUEST,
        )

    def composite_value_is_forbidden(self, data: Any) -> JSONResponse:
        return JSONResponse(
            content=super().composite_value_is_forbidden(data),
            status_code=HTTP_400_BAD_REQUEST,
        )


security = HTTPBasic()


def admin_only(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != 'admin' or credentials.password != 'admin':
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail='Incorrect email or password',
            headers={'WWW-Authenticate': 'Basic'},
        )


@app.post(
    '/nest/',
    dependencies=[Depends(admin_only)]
)
def nest(
        items: List[dict],
        keys: List[str] = Query(None),
):
    presenter = SanitiseJSONPresenter()

    if not keys:
        raise HTTPException(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                'loc': ['query', 'keys'],
                'msg': 'field required',
                'type': 'value_error.missing'
            }
        )

    elif not isinstance(items, list):
        return presenter.wrong_format()

    return GroupingUseCase(
        presenter=GroupingJSONPresenter(),
        data=items
    ).group_by(*keys)
