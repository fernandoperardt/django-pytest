import json
import pytest
from django.urls import reverse
from companies.models import Company

companies_url = reverse('companies-list')
pytestmark = pytest.mark.django_db

## GET
def test_zero_companies_should_return_empty_list(client) -> None:     
    response = client.get(companies_url)
    assert response.status_code == 200
    assert json.loads(response.content) == []

def test_one_compan_exists_should_succeed(client) -> None:
    amazon = Company.objects.create(name='Amazon')        
    response = client.get(companies_url)
    assert response.status_code == 200
    assert json.loads(response.content)[0].get('name') == 'Amazon'
    assert json.loads(response.content)[0].get('status') == 'Hiring'
## POST

def test_create_company_without_argument_should_fail(client):
    response = client.post(path=companies_url)
    assert response.status_code == 400
    assert json.loads(response.content) == {'name': ['This field is required.']}
    

def test_create_existing_company_should_fail(client):
    Company.objects.create(name='Amazon')
    response = client.post(path=companies_url, data={'name': 'Amazon'})
    assert response.status_code == 400
    assert json.loads(response.content) == {'name': ['company with this name already exists.']}
    

def test_create_company_with_only_name_all_fields_should_br_default(client):
    response = client.post(path=companies_url, data={'name': 'Amazon'})
    assert response.status_code == 201
    assert json.loads(response.content).get('name') == 'Amazon'
    assert json.loads(response.content).get('status') == 'Hiring'
    

def test_create_company_with_layoffs_status_shuould_succeed(client):
    response = client.post(path=companies_url, data={'name': 'Amazon', 'status': 'Layoffs'})
    assert response.status_code == 201
    assert json.loads(response.content).get('name') == 'Amazon'
    assert json.loads(response.content).get('status') == 'Layoffs'


def test_create_company_with_wrong_status_shuould_fail(client):
    response = client.post(path=companies_url, data={'name': 'Amazon', 'status': 'WrongStatus'})
    assert response.status_code == 400
    assert 'WrongStatus' in str(response.content)
    assert 'is not a valid choice' in str(response.content)

@pytest.mark.xfail
def test_shold_be_ok_if_fails():
    assert 1 == 2
    
@pytest.mark.skip
def test_shold_be_skipped():
    assert 1 == 2