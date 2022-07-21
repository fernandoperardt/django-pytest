# $ pytest . -v -p no:warnings
# $ pytest . -v -p no:warnings -m slow
# $ pytest . -v -p no:warnings -m 'not slow'
# $ pytest . -v -p no:warnings -s

import pytest
def test_our_first_test() -> None:
    assert 1 == 1

@pytest.mark.skip
def test_should_be_skipped():
    assert 1 == 2

@pytest.mark.skipif(4>1, reason='skipped because 4>1')
def test_should_be_skipped_if():
    assert 1 == 2

@pytest.mark.xfail
def test_dont_care_if_fails():
    assert 1 == 2

@pytest.mark.slow
def test_with_custom_mark1():
    assert 1 == 1

@pytest.mark.slow
def test_with_custom_mark2():
    assert 1 == 1


class Company():
    def __init__(self, name: str, stock_symbol: str) -> None:
        self.name = name
        self.stock_symbol = stock_symbol

    def __str__(self) -> str:
        return f'{self.name}:{self.stock_symbol}'

@pytest.fixture
def company() -> Company:
    return Company('Fiver', 'FVRR')

def test_with_fixture(company: Company):
    print(f'Printing {company} from fixture')

@pytest.mark.parametrize(
    'company_name',
    ['TikTok', 'Instagram', 'Twitch'],
    ids=['TikTok_test', 'Instagram_test', 'Twitch_test'],
)
def test_Paramtrized(company_name: str):
    print(f'\nTest with {company_name}')

def raise_covid19_exception():
    raise ValueError('CoronaVirus Exception')

def test_raise_covid19_exception_should_pass():
    with pytest.raises(ValueError) as e:
        raise_covid19_exception()
    assert 'CoronaVirus Exception' == str(e.value)