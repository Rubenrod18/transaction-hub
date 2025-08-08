from typing import Annotated
from uuid import UUID

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from starlette import status

from app.di_container import ServiceDIContainer
from app.exceptions import NotFoundException
from app.models import Transaction
from app.schemas import transaction_schemas
from app.services.transaction_service import TransactionService

router = APIRouter(prefix='/transactions', tags=['transactions'])


@router.post(
    '/',
    summary='Creates a new transaction',
    status_code=status.HTTP_201_CREATED,
    response_model=transaction_schemas.TransactionSchema,
    responses={
        201: {
            'description': 'Transaction created',
            'content': {
                'application/json': {
                    'schema': {'TransactionSchema': {'$ref': '#/components/schemas/TransactionSchema'}},
                    'examples': {
                        'TransactionWithPositiveAmount': {
                            '$ref': '#/components/examples/TransactionWithPositiveAmount'
                        },
                    },
                }
            },
        },
        400: {
            'description': 'Mandatory body parameters missing or have incorrect type',
        },
        405: {
            'description': 'Specified HTTP method not allowed',
        },
        415: {
            'description': 'Specified content type not allowed',
        },
    },
)
@inject
def create_transaction(
    payload: transaction_schemas.TransactionRequestSchema,
    transaction_service: Annotated[TransactionService, Depends(Provide[ServiceDIContainer.transaction_service])],
) -> Transaction:
    return transaction_service.create(**payload.model_dump())


@router.get(
    '/',
    summary='Returns a list of Transaction data',
    response_model=list[transaction_schemas.TransactionSchema],
    responses={
        200: {
            'description': 'A list of Transaction data',
            'content': {
                'application/json': {
                    'examples': {
                        'ArrayOfTransactionsExample': {'$ref': '#/components/examples/ArrayOfTransactionsExample'},
                    }
                }
            },
        },
    },
)
@inject
def get_transaction_list(
    transaction_service: Annotated[TransactionService, Depends(Provide[ServiceDIContainer.transaction_service])],
) -> list[Transaction]:
    return transaction_service.get()


@router.get(
    '/{transaction_id}',
    summary='Returns the transaction data',
    response_model=transaction_schemas.TransactionSchema,
    responses={
        200: {
            'description': 'Transaction data',
            'content': {
                'application/json': {
                    'examples': {
                        'TransactionWithPositiveAmount': {
                            '$ref': '#/components/examples/TransactionWithPositiveAmount'
                        },
                        'TransactionWithNegativeAmount': {
                            '$ref': '#/components/examples/TransactionWithNegativeAmount'
                        },
                    }
                }
            },
        },
        400: {
            'description': 'transaction_id missing or has incorrect type',
        },
        404: {
            'description': 'Transaction not found',
        },
    },
)
@inject
def get_transaction_details(
    transaction_id: UUID,
    transaction_service: Annotated[TransactionService, Depends(Provide[ServiceDIContainer.transaction_service])],
) -> Transaction:
    transaction = transaction_service.find_by_id(transaction_id)

    if transaction is None:
        raise NotFoundException(description='Transaction not found')

    return transaction
