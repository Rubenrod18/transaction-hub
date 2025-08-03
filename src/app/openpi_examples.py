examples = {
    'TransactionRequestWithPositiveAmount': {
        'value': {'account_id': '0afd02d3-6c59-46e7-b7bc-893c5e0b7ac2', 'amount': 7}
    },
    'TransactionRequestWithNegativeAmount': {
        'value': {'account_id': '5ae0ef78-e902-4c40-9f53-8cf910587312', 'amount': -4}
    },
    'TransactionWithPositiveAmount': {
        'value': {
            'transaction_id': '4bcc3959-6fe1-406e-9f04-cad2637b47d5',
            'account_id': '0afd02d3-6c59-46e7-b7bc-893c5e0b7ac2',
            'amount': 7,
            'created_at': '2023-06-14T22:20:27.031170',
            'updated_at': '2023-07-04T22:31:27.031170',
            'deleted_at': None,
        }
    },
    'TransactionWithNegativeAmount': {
        'value': {
            'transaction_id': '050a75f6-8df1-4ad1-8f5b-54e821e98581',
            'account_id': '5ae0ef78-e902-4c40-9f53-8cf910587312',
            'amount': -4,
            'created_at': '2023-06-14T22:20:27.031170',
            'updated_at': '2023-07-04T22:31:27.031170',
            'deleted_at': None,
        }
    },
    'ArrayOfTransactionsExample': {
        'value': [
            {
                'transaction_id': '4bcc3959-6fe1-406e-9f04-cad2637b47d5',
                'account_id': '0afd02d3-6c59-46e7-b7bc-893c5e0b7ac2',
                'amount': 7,
                'created_at': '2023-06-14T22:20:27.031170',
                'updated_at': '2023-07-04T22:31:27.031170',
                'deleted_at': None,
            },
            {
                'transaction_id': '050a75f6-8df1-4ad1-8f5b-54e821e98581',
                'account_id': '5ae0ef78-e902-4c40-9f53-8cf910587312',
                'amount': -4,
                'created_at': '2023-06-14T22:20:27.031170',
                'updated_at': '2023-07-04T22:31:27.031170',
                'deleted_at': None,
            },
        ]
    },
    'PositiveAccount': {
        'value': {
            'account_id': 'fbf4a552-2418-46c5-b308-6094ddc493a1',
            'balance': 10,
            'created_at': '2023-06-14T22:20:27.031170',
            'updated_at': '2023-07-04T22:31:27.031170',
            'deleted_at': None,
        }
    },
    'NegativeAccount': {
        'value': {
            'account_id': '9c3cd9a8-65c4-4d26-8488-ef9a40f57c37',
            'balance': -75,
            'created_at': '2023-06-14T22:20:27.031170',
            'updated_at': '2023-07-04T22:31:27.031170',
            'deleted_at': '2023-07-04T22:31:27.031170',
        }
    },
}
