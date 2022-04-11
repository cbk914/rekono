from typing import Any, Dict
from unittest import mock

from testing.api.base import RekonoTestCase
from testing.mocks.defectdojo import (defect_dojo_error, defect_dojo_success,
                                      defect_dojo_success_multiple)


class ProjectsTest(RekonoTestCase):
    '''Test cases for Projects module.'''

    def setUp(self) -> None:
        '''Create initial data before run tests.'''
        self.endpoint = '/api/projects/'                                        # Projects API endpoint
        super().setUp()
        # Data for testing
        self.used_data = {'name': self.project.name, 'description': self.project.description, 'tags': self.project.tags}
        self.new_data: Dict[str, Any] = {'name': 'New Test', 'description': 'New Test', 'tags': ['new']}
        self.models = {self.project: self.project.name}                         # Models to test __str__ method

    def test_create(self) -> None:
        '''Test project creation feature.'''
        # Create new project
        self.api_test(self.client.post, self.endpoint, 201, data=self.new_data, expected=self.new_data)

    # @mock.patch('defectdojo.api.DefectDojo.request', defect_dojo_success)       # Mocks Defect-Dojo response
    # def test_create_with_defect_dojo_product(self) -> None:
    #     '''Test project creation feature with valid Defect-Dojo product Id.'''
    #     self.new_data['defectdojo_product_id'] = 1
    #     # Create new project
    #     self.api_test(self.client.post, self.endpoint, 201, data=self.new_data, expected=self.new_data)

    def test_invalid_create(self) -> None:
        '''Test project creation feature with invalid data.'''
        self.api_test(self.client.post, self.endpoint, 400, data=self.used_data)    # Project already exists

    # @mock.patch('defectdojo.api.DefectDojo.request', defect_dojo_error)         # Mocks Defect-Dojo response
    # def test_invalid_create_with_defect_dojo_product_not_found(self) -> None:
    #     '''Test project creation feature with not found Defect-Dojo product Id.'''
    #     self.new_data['defectdojo_product_id'] = 1
    #     # Defect-Dojo product Id doesn't exist
    #     self.api_test(self.client.post, self.endpoint, 400, data=self.new_data)

    def test_update(self) -> None:
        '''Test project update feature.'''
        # Update project
        self.api_test(self.client.put, f'{self.endpoint}{self.project.id}/', data=self.new_data, expected=self.new_data)

    def test_invalid_update(self) -> None:
        '''Test project update feature with invalid data.'''
        # Create new project
        content = self.api_test(self.client.post, self.endpoint, 201, data=self.new_data, expected=self.new_data)
        # Project already exists
        self.api_test(self.client.put, f'{self.endpoint}{content["id"]}/', 400, data=self.used_data)

    def test_delete(self) -> None:
        '''Test project deletion feature.'''
        self.api_test(self.client.delete, f'{self.endpoint}{self.project.id}/', 204)                # Delete new project
        self.api_test(self.client.get, f'{self.endpoint}{self.project.id}/', 404)

    def test_add_member(self) -> None:
        '''Test add project member feature.'''
        # Add member to the testing project
        self.api_test(self.client.post, f'{self.endpoint}{self.project.id}/members/', 201, data={'user': self.other.id})

    def test_add_not_found_member(self) -> None:
        '''Test add project member feature with not found user.'''
        # Add unexisting member to the testing project
        self.api_test(self.client.post, f'{self.endpoint}{self.project.id}/members/', 404, data={'user': -1})

    def test_add_invalid_member(self) -> None:
        '''Test add project member feature with invalid data.'''
        self.api_test(self.client.post, f'{self.endpoint}{self.project.id}/members/', 400)          # User is required

    def test_remove_member(self) -> None:
        '''Test remove project member feature.'''
        # Add member to the testing project
        self.api_test(self.client.post, f'{self.endpoint}{self.project.id}/members/', 201, data={'user': self.other.id})
        # Remove project member
        self.api_test(self.client.delete, f'{self.endpoint}{self.project.id}/members/{self.other.id}/', 204)

    def test_remove_not_found_member(self) -> None:
        '''Test remove project member feature with not found user.'''
        # Remove unexisting member from testing project
        self.api_test(self.client.delete, f'{self.endpoint}{self.project.id}/members/0/', 404)

    def test_remove_invalid_member(self) -> None:
        '''Test remove project member feature with invalid data.'''
        # Project owner can't be removed
        self.api_test(self.client.delete, f'{self.endpoint}{self.project.id}/members/{self.admin.id}/', 400)

    @mock.patch('defectdojo.api.DefectDojo.request', defect_dojo_error)         # Mocks Defect-Dojo response
    def test_defectdojo_unavailable(self) -> None:
        self.api_test(self.client.put, f'{self.endpoint}{self.project.id}/defect-dojo/', 400)

    @mock.patch('defectdojo.api.DefectDojo.request', defect_dojo_success)       # Mocks Defect-Dojo response
    @mock.patch('defectdojo.api.DefectDojo.get_rekono_product_type', defect_dojo_success_multiple)
    def test_defectdojo_with_ids(self) -> None:
        self.api_test(
            self.client.put, f'{self.endpoint}{self.project.id}/defect-dojo/', 200,
            data={'product_id': 1, 'engagement_id': 1},
            expected={
                'defectdojo_product_id': 1,
                'defectdojo_engagement_id': 1,
                'defectdojo_engagement_by_target': False
            }
        )

    @mock.patch('defectdojo.api.DefectDojo.request', defect_dojo_success)       # Mocks Defect-Dojo response
    def test_defectdojo_with_new_product(self) -> None:
        self.api_test(
            self.client.put, f'{self.endpoint}{self.project.id}/defect-dojo/', 200,
            data={'engagement_id': 1},
            expected={
                'defectdojo_product_id': 1,
                'defectdojo_engagement_id': 1,
                'defectdojo_engagement_by_target': False
            }
        )

    @mock.patch('defectdojo.api.DefectDojo.request', defect_dojo_success)       # Mocks Defect-Dojo response
    def test_defectdojo_with_new_engagement(self) -> None:
        self.api_test(
            self.client.put, f'{self.endpoint}{self.project.id}/defect-dojo/', 200,
            data={'product_id': 1, 'engagement_name': 'Test', 'engagement_description': 'Test'},
            expected={
                'defectdojo_product_id': 1,
                'defectdojo_engagement_id': 1,
                'defectdojo_engagement_by_target': False
            }
        )

    @mock.patch('defectdojo.api.DefectDojo.request', defect_dojo_success)       # Mocks Defect-Dojo response
    def test_defectdojo_with_new_product_and_engagemnets_per_target(self) -> None:
        self.api_test(
            self.client.put, f'{self.endpoint}{self.project.id}/defect-dojo/', 200,
            expected={
                'defectdojo_product_id': 1,
                'defectdojo_engagement_id': None,
                'defectdojo_engagement_by_target': True
            }
        )

    @mock.patch('defectdojo.api.DefectDojo.request', defect_dojo_success)       # Mocks Defect-Dojo response
    @mock.patch('defectdojo.api.DefectDojo.get_engagement', defect_dojo_error)
    def test_defectdojo_with_engagement_not_found(self) -> None:
        self.api_test(self.client.put, f'{self.endpoint}{self.project.id}/defect-dojo/', 400, data={'engagement_id': 1})

    @mock.patch('defectdojo.api.DefectDojo.request', defect_dojo_success)       # Mocks Defect-Dojo response
    @mock.patch('defectdojo.api.DefectDojo.get_product', defect_dojo_error)
    def test_defectdojo_with_product_not_found(self) -> None:
        self.api_test(self.client.put, f'{self.endpoint}{self.project.id}/defect-dojo/', 400, data={'product_id': 1})

    @mock.patch('defectdojo.api.DefectDojo.request', defect_dojo_success)       # Mocks Defect-Dojo response
    def test_defectdojo_with_invalid_new_engagement(self) -> None:
        self.api_test(
            self.client.put, f'{self.endpoint}{self.project.id}/defect-dojo/', 400,
            data={'product_id': 1, 'engagement_name': 'Input;Validation', 'engagement_description': 'Input;Validation'}
        )

    @mock.patch('defectdojo.api.DefectDojo.request', defect_dojo_success)       # Mocks Defect-Dojo response
    @mock.patch('defectdojo.api.DefectDojo.create_rekono_product_type', defect_dojo_error)
    def test_defectdojo_with_error_in_product_type_creation(self) -> None:
        self.api_test(self.client.put, f'{self.endpoint}{self.project.id}/defect-dojo/', 400)

    @mock.patch('defectdojo.api.DefectDojo.request', defect_dojo_success)       # Mocks Defect-Dojo response
    @mock.patch('defectdojo.api.DefectDojo.create_product', defect_dojo_error)
    def test_defectdojo_with_error_in_product_creation(self) -> None:
        self.api_test(self.client.put, f'{self.endpoint}{self.project.id}/defect-dojo/', 400)

    @mock.patch('defectdojo.api.DefectDojo.request', defect_dojo_success)       # Mocks Defect-Dojo response
    @mock.patch('defectdojo.api.DefectDojo.create_engagement', defect_dojo_error)
    def test_defectdojo_with_error_in_engagement_creation(self) -> None:
        self.api_test(
            self.client.put, f'{self.endpoint}{self.project.id}/defect-dojo/', 400,
            data={'product_id': 1, 'engagement_name': 'Test', 'engagement_description': 'Test'}
        )

    @mock.patch('defectdojo.api.DefectDojo.request', defect_dojo_success)       # Mocks Defect-Dojo response
    def test_defectdojo_sync(self) -> None:
        self.api_test(
            self.client.put, f'{self.endpoint}{self.project.id}/defect-dojo/', 200,
            expected={
                'defectdojo_product_id': 1,
                'defectdojo_engagement_id': None,
                'defectdojo_engagement_by_target': True,
                'defectdojo_synchronization': False
            }
        )
        self.api_test(
            self.client.put, f'{self.endpoint}{self.project.id}/defect-dojo/sync/', 200,
            data={'synchronization': True},
            expected={
                'defectdojo_product_id': 1,
                'defectdojo_engagement_id': None,
                'defectdojo_engagement_by_target': True,
                'defectdojo_synchronization': True
            }
        )

    def test_invalid_defectdojo_sync(self) -> None:
        self.api_test(
            self.client.put, f'{self.endpoint}{self.project.id}/defect-dojo/sync/', 400, data={'synchronization': True}
        )
        self.api_test(self.client.put, f'{self.endpoint}{self.project.id}/defect-dojo/sync/', 400)
