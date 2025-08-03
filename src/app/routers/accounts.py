from typing import Annotated
from uuid import UUID

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from app.di_container import ServiceDIContainer
from app.exceptions import NotFoundException
from app.models import Account
from app.schemas import account_schemas
from app.services.account_service import AccountService

router = APIRouter(prefix='/accounts', tags=['accounts'])


@router.get(
    '/',
    summary='Returns a list of Account data',
    response_model=list[account_schemas.AccountSchema],
    responses={
        200: {
            'description': 'A list of Account data',
            'content': {
                'application/json': {
                    'examples': {
                        'PositiveAccount': {'$ref': '#/components/examples/PositiveAccount'},
                        'NegativeAccount': {'$ref': '#/components/examples/NegativeAccount'},
                    }
                }
            },
        },
    },
)
@inject
def get_account_list(
    account_service: Annotated[AccountService, Depends(Provide[ServiceDIContainer.account_service])],
) -> list[Account]:
    return account_service.get()


@router.get(
    '/{account_id}',
    summary='Returns the Account data',
    response_model=account_schemas.AccountSchema,
    responses={
        200: {
            'description': 'Account data',
            'content': {
                'application/json': {
                    'examples': {
                        'PositiveAccount': {'$ref': '#/components/examples/PositiveAccount'},
                        'NegativeAccount': {'$ref': '#/components/examples/NegativeAccount'},
                    }
                }
            },
        },
        400: {
            'description': 'account_id missing or has incorrect type',
        },
        404: {
            'description': 'Account not found',
        },
    },
)
@inject
def get_account_details(
    account_id: UUID, account_service: Annotated[AccountService, Depends(Provide[ServiceDIContainer.account_service])]
) -> Account:
    account = account_service.find_by_id(account_id)

    if account is None:
        raise NotFoundException(description='Account not found')

    return account
