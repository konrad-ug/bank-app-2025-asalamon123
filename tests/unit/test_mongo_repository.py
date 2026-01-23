import pytest
from unittest.mock import Mock
from src.mongo_repository import MongoAccountsRepository
from src.account import Account
from app.api import registry



@pytest.fixture(autouse=True)
def clear_registry():
    registry.clear_all()

@pytest.fixture
def sample_accounts():
    acc1 = Account("Adam", "Kowalski", "12345678901", None)
    acc2 = Account("Ewa", "Nowak", "98765432109", None)
    return [acc1, acc2]


def test_save_all(sample_accounts):
    mock_collection = Mock()
    repo = MongoAccountsRepository(collection=mock_collection)

    repo.save_all(sample_accounts)

    mock_collection.delete_many.assert_called_once_with({})

    assert mock_collection.update_one.call_count == len(sample_accounts)

def test_load_all(sample_accounts):
    mock_docs = [
        {
            "first_name": acc.first_name,
            "last_name": acc.last_name,
            "pesel": acc.pesel,
            "promo_code": acc.promo_code,
        } for acc in sample_accounts
    ]

    mock_collection = Mock()
    mock_collection.find.return_value = mock_docs

    repo = MongoAccountsRepository(collection=mock_collection)
    accounts = repo.load_all()

    assert len(accounts) == len(sample_accounts)

    assert accounts[0].pesel == sample_accounts[0].pesel
    assert accounts[1].first_name == sample_accounts[1].first_name