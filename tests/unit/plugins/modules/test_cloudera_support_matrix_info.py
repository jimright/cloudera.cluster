#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2024 Cloudera, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Unit tests for cloudera_support_matrix_info module.
"""

import json
import pytest
import requests
from unittest.mock import MagicMock, patch
from ansible.module_utils.basic import AnsibleModule

from ansible_collections.cloudera.cluster.plugins.modules import cloudera_support_matrix_info
from ansible_collections.cloudera.cluster.tests.unit import (
    AnsibleExitJson,
    AnsibleFailJson,
)


class TestClouderaSupportMatrixInfo:
    """Test class for ClouderaSupportMatrixInfo."""

    @pytest.fixture
    def mock_module(self):
        """Create a mock AnsibleModule instance."""
        module = MagicMock()
        module.params = {
            'product_name': None,
            'product_version': None,
            'operating_system': None,
            'jdk': None,
            'database': None,
            'processor': None,
            'kubernetes': None,
            'timeout': 30
        }
        return module

    @pytest.fixture
    def sample_api_response(self):
        """Sample API response data for testing."""
        return {
            "browsers": [],
            "databases": [
                {
                    "version": "13",
                    "family": "PostgreSQL",
                    "description": "PostgreSQL-13",
                    "id": 801
                }
            ],
            "jdks": [
                {
                    "description": "OpenJDK-JDK11",
                    "version": "JDK11",
                    "family": "OpenJDK",
                    "id": 797
                }
            ],
            "products": [
                {
                    "version": "7.13.1",
                    "productName": "Cloudera Manager",
                    "description": "Cloudera Manager-7.13.1",
                    "id": 1325,
                    "group": "7.13"
                },
                {
                    "version": "7.1.9",
                    "productName": "CDP Private Cloud Base",
                    "description": "CDP Private Cloud Base-7.1.9",
                    "id": 869,
                    "group": "7.1"
                }
            ],
            "kubernetes": [],
            "processor": [],
            "operatingSystems": [
                {
                    "description": "Rocky Linux-9.4",
                    "version": "9.4",
                    "family": "Rocky Linux",
                    "id": 1087,
                    "group": "9"
                }
            ]
        }

    def test_init_basic(self, mock_module):
        """Test basic initialization of ClouderaSupportMatrixInfo."""
        matrix_info = cloudera_support_matrix_info.ClouderaSupportMatrixInfo(mock_module)
        
        assert matrix_info.module == mock_module
        assert matrix_info.product_name is None
        assert matrix_info.product_version is None
        assert matrix_info.timeout == 30
        assert matrix_info.api_url == "https://supportmatrix.cloudera.com/supportmatrices/cldr"

    def test_init_with_params(self, mock_module):
        """Test initialization with parameters."""
        mock_module.params.update({
            'product_name': 'Cloudera Manager',
            'product_version': '7.13.1',
            'operating_system': 'RHEL-8.8',
            'timeout': 60
        })
        
        matrix_info = cloudera_support_matrix_info.ClouderaSupportMatrixInfo(mock_module)
        
        assert matrix_info.product_name == 'Cloudera Manager'
        assert matrix_info.product_version == '7.13.1'
        assert matrix_info.operating_system == 'RHEL-8.8'
        assert matrix_info.timeout == 60

    def test_build_query_conditions_no_filters(self, mock_module):
        """Test building query conditions with no filters."""
        matrix_info = cloudera_support_matrix_info.ClouderaSupportMatrixInfo(mock_module)
        
        conditions = matrix_info._build_query_conditions()
        
        assert conditions == ""
        assert matrix_info.filters_applied == {}

    def test_build_query_conditions_with_product(self, mock_module):
        """Test building query conditions with product name and version."""
        mock_module.params.update({
            'product_name': 'Cloudera Manager',
            'product_version': '7.13.1'
        })
        
        matrix_info = cloudera_support_matrix_info.ClouderaSupportMatrixInfo(mock_module)
        conditions = matrix_info._build_query_conditions()
        
        assert conditions == "PRODUCT=Cloudera Manager-7.13.1"
        assert matrix_info.filters_applied['product_name'] == 'Cloudera Manager'
        assert matrix_info.filters_applied['product_version'] == '7.13.1'

    def test_build_query_conditions_with_multiple_filters(self, mock_module):
        """Test building query conditions with multiple filters."""
        mock_module.params.update({
            'product_name': 'Cloudera Manager',
            'product_version': '7.13.1',
            'operating_system': 'Rocky Linux-9.4',
            'jdk': 'OpenJDK-JDK11'
        })
        
        matrix_info = cloudera_support_matrix_info.ClouderaSupportMatrixInfo(mock_module)
        conditions = matrix_info._build_query_conditions()
        
        expected_conditions = [
            "PRODUCT=Cloudera Manager-7.13.1",
            "OPERATING_SYSTEM=Rocky Linux-9.4",
            "JDK=OpenJDK-JDK11"
        ]
        
        for condition in expected_conditions:
            assert condition in conditions

    def test_build_query_conditions_product_name_only(self, mock_module):
        """Test building query conditions with only product name (no version)."""
        mock_module.params.update({
            'product_name': 'Cloudera Manager'
        })
        
        matrix_info = ClouderaSupportMatrixInfo(mock_module)
        conditions = matrix_info._build_query_conditions()
        
        # Should not include PRODUCT condition, only add to filters_applied
        assert "PRODUCT=" not in conditions
        assert matrix_info.filters_applied['product_name'] == 'Cloudera Manager'

    def test_build_api_url_no_conditions(self, mock_module):
        """Test API URL building with no conditions."""
        matrix_info = ClouderaSupportMatrixInfo(mock_module)
        
        api_url = matrix_info._build_api_url()
        
        assert api_url == "https://supportmatrix.cloudera.com/supportmatrices/cldr"

    def test_build_api_url_with_conditions(self, mock_module):
        """Test API URL building with conditions."""
        mock_module.params.update({
            'product_name': 'Cloudera Manager',
            'product_version': '7.13.1',
            'operating_system': 'Rocky Linux-9.4'
        })
        
        matrix_info = ClouderaSupportMatrixInfo(mock_module)
        api_url = matrix_info._build_api_url()
        
        assert api_url.startswith("https://supportmatrix.cloudera.com/supportmatrices/cldr?condition=")
        assert "PRODUCT=Cloudera Manager-7.13.1" in api_url
        assert "OPERATING_SYSTEM=Rocky Linux-9.4" in api_url

    def test_filter_products_by_name(self, mock_module, sample_api_response):
        """Test filtering products by name."""
        mock_module.params.update({
            'product_name': 'Cloudera Manager'
        })
        
        matrix_info = ClouderaSupportMatrixInfo(mock_module)
        filtered_data = matrix_info._filter_products_by_name(sample_api_response)
        
        assert len(filtered_data['products']) == 1
        assert filtered_data['products'][0]['productName'] == 'Cloudera Manager'

    def test_filter_products_by_name_no_filter(self, mock_module, sample_api_response):
        """Test that products are not filtered when no product_name is specified."""
        matrix_info = ClouderaSupportMatrixInfo(mock_module)
        filtered_data = matrix_info._filter_products_by_name(sample_api_response)
        
        # Should return original data unchanged
        assert len(filtered_data['products']) == 2

    @patch('ansible_collections.cloudera.cluster.plugins.modules.cloudera_support_matrix_info.requests.get')
    def test_fetch_support_matrix_data_success(self, mock_requests_get, mock_module, sample_api_response):
        """Test successful API data fetching."""
        # Mock successful response
        mock_response = MagicMock()
        mock_response.text = json.dumps(sample_api_response)
        mock_response.raise_for_status.return_value = None
        mock_requests_get.return_value = mock_response
        
        matrix_info = ClouderaSupportMatrixInfo(mock_module)
        success = matrix_info.fetch_support_matrix_data()
        
        assert success is True
        assert matrix_info.support_matrix_data == sample_api_response

    @patch('ansible_collections.cloudera.cluster.plugins.modules.cloudera_support_matrix_info.requests.get')
    def test_fetch_support_matrix_data_http_error(self, mock_requests_get, mock_module):
        """Test handling of HTTP errors."""
        # Mock HTTP error response
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
        mock_requests_get.return_value = mock_response
        
        matrix_info = ClouderaSupportMatrixInfo(mock_module)
        success = matrix_info.fetch_support_matrix_data()
        
        assert success is False
        mock_module.fail_json.assert_called_once()

    @patch('ansible_collections.cloudera.cluster.plugins.modules.cloudera_support_matrix_info.requests.get')
    def test_fetch_support_matrix_data_json_error(self, mock_requests_get, mock_module):
        """Test handling of JSON parsing errors."""
        # Mock response with invalid JSON
        mock_response = MagicMock()
        mock_response.text = "invalid json content"
        mock_response.raise_for_status.return_value = None
        mock_requests_get.return_value = mock_response
        
        matrix_info = ClouderaSupportMatrixInfo(mock_module)
        success = matrix_info.fetch_support_matrix_data()
        
        assert success is False
        mock_module.fail_json.assert_called_once()

    @patch('ansible_collections.cloudera.cluster.plugins.modules.cloudera_support_matrix_info.requests.get')
    def test_fetch_support_matrix_data_empty_response(self, mock_requests_get, mock_module):
        """Test handling of empty responses."""
        mock_response = MagicMock()
        mock_response.text = ""
        mock_response.raise_for_status.return_value = None
        mock_requests_get.return_value = mock_response
        
        matrix_info = ClouderaSupportMatrixInfo(mock_module)
        success = matrix_info.fetch_support_matrix_data()
        
        assert success is False
        mock_module.fail_json.assert_called_once()

    @patch('ansible_collections.cloudera.cluster.plugins.modules.cloudera_support_matrix_info.requests.get')
    def test_fetch_support_matrix_data_with_filtering(self, mock_requests_get, mock_module, sample_api_response):
        """Test API data fetching with product name filtering."""
        mock_module.params.update({
            'product_name': 'Cloudera Manager'
        })
        
        # Mock successful response
        mock_response = MagicMock()
        mock_response.text = json.dumps(sample_api_response)
        mock_response.raise_for_status.return_value = None
        mock_requests_get.return_value = mock_response
        
        matrix_info = ClouderaSupportMatrixInfo(mock_module)
        success = matrix_info.fetch_support_matrix_data()
        
        assert success is True
        # Should only have Cloudera Manager products
        assert len(matrix_info.support_matrix_data['products']) == 1
        assert matrix_info.support_matrix_data['products'][0]['productName'] == 'Cloudera Manager'


class TestMainFunction:
    """Test the main function."""

    @patch('ansible_collections.cloudera.cluster.plugins.modules.cloudera_support_matrix_info.AnsibleModule')
    @patch('ansible_collections.cloudera.cluster.plugins.modules.cloudera_support_matrix_info.ClouderaSupportMatrixInfo')
    def test_main_success(self, mock_matrix_class, mock_ansible_module):
        """Test successful execution of main function."""
        # Mock module
        mock_module = MagicMock()
        mock_module.params = {
            'product_version': None,
            'product_name': None
        }
        mock_ansible_module.return_value = mock_module
        
        # Mock matrix info instance
        mock_matrix_instance = MagicMock()
        mock_matrix_instance.fetch_support_matrix_data.return_value = True
        mock_matrix_instance.support_matrix_data = {"test": "data"}
        mock_matrix_instance.filters_applied = {"product_name": "test"}
        mock_matrix_instance.api_url = "http://test.com"
        mock_matrix_class.return_value = mock_matrix_instance
        
        main()
        
        # Verify module was called with expected arguments
        mock_ansible_module.assert_called_once()
        mock_matrix_instance.fetch_support_matrix_data.assert_called_once()
        mock_module.exit_json.assert_called_once()

    @patch('ansible_collections.cloudera.cluster.plugins.modules.cloudera_support_matrix_info.AnsibleModule')
    def test_main_product_version_without_name(self, mock_ansible_module):
        """Test main function with product_version but no product_name."""
        mock_module = MagicMock()
        mock_module.params = {
            'product_version': '7.13.1',
            'product_name': None
        }
        mock_ansible_module.return_value = mock_module
        
        main()
        
        # Should fail with appropriate error
        mock_module.fail_json.assert_called_once_with(
            msg="product_version requires product_name to be specified"
        )

    @patch('ansible_collections.cloudera.cluster.plugins.modules.cloudera_support_matrix_info.AnsibleModule')
    @patch('ansible_collections.cloudera.cluster.plugins.modules.cloudera_support_matrix_info.ClouderaSupportMatrixInfo')
    def test_main_fetch_failure(self, mock_matrix_class, mock_ansible_module):
        """Test main function when data fetching fails."""
        # Mock module
        mock_module = MagicMock()
        mock_module.params = {
            'product_version': None,
            'product_name': None
        }
        mock_ansible_module.return_value = mock_module
        
        # Mock matrix info instance with failure
        mock_matrix_instance = MagicMock()
        mock_matrix_instance.fetch_support_matrix_data.return_value = False
        mock_matrix_class.return_value = mock_matrix_instance
        
        main()
        
        # Should fail
        mock_module.fail_json.assert_called_once_with(
            msg="Unknown error occurred while fetching support matrix data"
        )


if __name__ == "__main__":
    pytest.main([__file__]) 