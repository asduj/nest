from typing import List, Any, Tuple

from fastapi import FastAPI, Query, Depends, HTTPException
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from starlette.responses import JSONResponse
from starlette.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from nest import GroupingUseCase, GroupingPresenter

app = FastAPI()


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

    def limited_keys_number(self, keys: Tuple[str, ...]) -> JSONResponse:
        return JSONResponse(
            content=super().limited_keys_number(keys),
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
    if not keys:
        # Hack to make an error similar built-in validation error
        # Because Query(None) make `keys` optional
        raise HTTPException(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                'loc': ['query', 'keys'],
                'msg': 'field required',
                'type': 'value_error.missing'
            }
        )

    return GroupingUseCase(
        presenter=GroupingJSONPresenter(),
        data=items
    ).group_by(*keys)
