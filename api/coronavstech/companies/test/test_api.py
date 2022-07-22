import json
import pytest
from unittest import TestCase
from django.test import Client
from django.urls import reverse
from companies.models import Company

@pytest.mark.django_db
class BasicCompanyApiTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.companies_url = reverse('companies-list')
        
        
    def tearDown(self) -> None:
        pass


class TestGetCompanies(BasicCompanyApiTestCase):
    
    def test_zero_companies_should_return_empty_list(self) -> None:     
        response = self.client.get(self.companies_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), [])
        
    def test_one_compan_exists_should_succeed(self) -> None:
        amazon = Company.objects.create(name='Amazon')        
        response = self.client.get(self.companies_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)[0].get('name'), 'Amazon')
        self.assertEqual(json.loads(response.content)[0].get('status'), 'Hiring')
        
        amazon.delete()
        
class TestPostCompanies(BasicCompanyApiTestCase):
    def test_create_company_without_argument_should_fail(self):
        response = self.client.post(path=self.companies_url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), {'name': ['This field is required.']})
        
        
    def test_create_existing_company_should_fail(self):
        Company.objects.create(name='Amazon')
        response = self.client.post(path=self.companies_url, data={'name': 'Amazon'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), {'name': ['company with this name already exists.']})
        
        
    def test_create_company_with_only_name_all_fields_should_br_default(self):
        response = self.client.post(path=self.companies_url, data={'name': 'Amazon'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.content).get('name'), 'Amazon')
        self.assertEqual(json.loads(response.content).get('status'), 'Hiring')
        
        
    def test_create_company_with_layoffs_status_shuould_succeed(self):
        response = self.client.post(path=self.companies_url, data={'name': 'Amazon', 'status': 'Layoffs'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.content).get('name'), 'Amazon')
        self.assertEqual(json.loads(response.content).get('status'), 'Layoffs')
        
    def test_create_company_with_wrong_status_shuould_fail(self):
        response = self.client.post(path=self.companies_url, data={'name': 'Amazon', 'status': 'WrongStatus'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('WrongStatus', str(response.content))
        self.assertIn('is not a valid choice', str(response.content))

    @pytest.mark.xfail
    def test_shold_be_ok_if_fails(self):
        self.assertEqual(1, 2)
        
    @pytest.mark.skip
    def test_shold_be_skipped(self):
        self.assertEqual(1, 2)