#!/usr/bin/python
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

DOCUMENTATION = r"""
module: cloudera_support_matrix_info
short_description: Retrieve Cloudera Support Matrix information
description:
  - Retrieve product compatibility and support information from the Cloudera Support Matrix API.
  - Supports filtering by various criteria including multiple product versions, OS, JDK, database, processor, and Kubernetes.
  - Returns comprehensive support matrix data including compatibility information across different Cloudera products.
author:
  - "Jim Enright (@jimright)"
version_added: "5.0.0"
requirements:
  - requests (Python library)
options:
  cloudera_manager_version:
    description:
      - Filter by specific Cloudera Manager version.
      - Examples include '7.13.1', '7.11.3', '7.10.1'.
    type: str
    required: false
  cloudera_runtime_version:
    description:
      - Filter by specific CDP Private Cloud Base (Cloudera Runtime) version.
      - Examples include '7.1.9', '7.1.9 SP1', '7.3.1'.
    type: str
    required: false
  cloudera_data_services_version:
    description:
      - Filter by specific CDP Private Cloud Data Services version.
      - Examples include '1.5.4', '1.5.4 SP1', '1.5.5'.
    type: str
    required: false
  cloudera_flow_management_version:
    description:
      - Filter by specific Cloudera Flow Management version.
      - Examples include '2.1.7', '4.10.0', '4.0.0'.
    type: str
    required: false
  cloudera_streaming_analytics_version:
    description:
      - Filter by specific Cloudera Streaming Analytics version.
      - Examples include '1.13.2', '1.15.0', '1.14.1'.
    type: str
    required: false
  cloudera_data_visualization_version:
    description:
      - Filter by specific Cloudera Data Visualization version.
      - Examples include '8.0.3'.
    type: str
    required: false
  cds_spark_version:
    description:
      - Filter by specific CDS Powered by Apache Spark version.
      - Examples include '3.3.2', '3.2.3', '3.1.1'.
    type: str
    required: false
  python_version:
    description:
      - Filter by specific Python version.
      - Examples include '3.10', '3.9', '3.8', '2.7'.
    type: str
    required: false
  operating_system:
    description:
      - Filter by operating system.
      - Format should be 'OS_Family-Version' (e.g., 'RHEL-8.8', 'Rocky Linux-9.4').
    type: str
    required: false
  jdk:
    description:
      - Filter by JDK version and family.
      - Format should be 'JDK_Family-Version' (e.g., 'OpenJDK-JDK11', 'OracleJDK-JDK8').
    type: str
    required: false
  database:
    description:
      - Filter by database type and version.
      - Format should be 'Database_Family-Version' (e.g., 'PostgreSQL-13', 'MySQL-8.0').
    type: str
    required: false
  processor:
    description:
      - Filter by processor architecture.
      - Examples include 'x86-x86-64', 'IBM Power Systems-Power 9'.
    type: str
    required: false
  kubernetes:
    description:
      - Filter by Kubernetes platform.
      - Format should be 'Platform-Version' (e.g., 'OCP-4.16').
    type: str
    required: false
  timeout:
    description:
      - HTTP request timeout in seconds.
    type: int
    default: 30
  validate_certs:
    description:
      - Whether to validate SSL certificates.
    type: bool
    default: true
"""

EXAMPLES = r"""
- name: Get all support matrix information
  cloudera.cluster.cloudera_support_matrix_info:
  register: full_matrix

- name: Get support matrix for multiple Cloudera products
  cloudera.cluster.cloudera_support_matrix_info:
    cloudera_manager_version: "7.13.1"
    cloudera_runtime_version: "7.1.9 SP1"
    cloudera_data_services_version: "1.5.4"
  register: multi_product_matrix

- name: Get support matrix for Cloudera Manager with specific OS and JDK
  cloudera.cluster.cloudera_support_matrix_info:
    cloudera_manager_version: "7.11.3"
    operating_system: "Rocky Linux-9.4"
    jdk: "OpenJDK-JDK11"
  register: cm_rocky_matrix

- name: Get support matrix for CDP stack with database
  cloudera.cluster.cloudera_support_matrix_info:
    cloudera_runtime_version: "7.1.9"
    operating_system: "RHEL-8.8"
    database: "PostgreSQL-13"
  register: cdp_base_matrix

- name: Get support matrix for Streaming Analytics
  cloudera.cluster.cloudera_support_matrix_info:
    cloudera_streaming_analytics_version: "1.13.2"
    python_version: "3.9"
  register: csa_matrix

- name: Get support matrix for Flow Management
  cloudera.cluster.cloudera_support_matrix_info:
    cloudera_flow_management_version: "2.1.7"
    jdk: "OpenJDK-JDK11"
  register: cfm_matrix

- name: Get support matrix with custom timeout
  cloudera.cluster.cloudera_support_matrix_info:
    cloudera_data_services_version: "1.5.4"
    timeout: 60
  register: cdp_ds_matrix

- name: Get support matrix for Rocky Linux only
  cloudera.cluster.cloudera_support_matrix_info:
    operating_system: "Rocky Linux-9.4"
  register: rocky_matrix

- name: Get support matrix for complete CDP stack
  cloudera.cluster.cloudera_support_matrix_info:
    cloudera_manager_version: "7.13.1"
    cloudera_runtime_version: "7.1.9 SP1"
    cloudera_data_services_version: "1.5.5"
    operating_system: "RHEL-9.5"
  register: complete_stack_matrix

- name: Disable SSL certificate validation
  cloudera.cluster.cloudera_support_matrix_info:
    cloudera_manager_version: "7.13.1"
    validate_certs: false
  register: matrix_no_ssl_validation
"""

RETURN = r"""
support_matrix_data:
    description: Complete support matrix information from Cloudera
    type: dict
    returned: always
    contains:
        browsers:
            description: Browser support information
            type: list
            returned: always
        databases:
            description: Database compatibility information
            type: list
            returned: always
            sample: [
                {
                    "version": "13",
                    "family": "PostgreSQL", 
                    "description": "PostgreSQL-13",
                    "id": 801
                }
            ]
        jdks:
            description: JDK compatibility information
            type: list
            returned: always
            sample: [
                {
                    "version": "JDK11",
                    "family": "OpenJDK",
                    "description": "OpenJDK-JDK11",
                    "id": 797
                }
            ]
        products:
            description: Cloudera product information
            type: list
            returned: always
            sample: [
                {
                    "version": "7.13.1",
                    "productName": "Cloudera Manager",
                    "description": "Cloudera Manager-7.13.1",
                    "id": 1325,
                    "group": "7.13"
                }
            ]
        kubernetes:
            description: Kubernetes platform compatibility
            type: list
            returned: always
        processor:
            description: Processor architecture compatibility
            type: list
            returned: always
        operatingSystems:
            description: Operating system compatibility
            type: list
            returned: always
            sample: [
                {
                    "version": "9.4",
                    "family": "Rocky Linux",
                    "description": "Rocky Linux-9.4",
                    "id": 1087,
                    "group": "9"
                }
            ]
filters_applied:
    description: Summary of filters that were applied to the API request
    type: dict
    returned: always
    contains:
        cloudera_manager_version:
            description: Cloudera Manager version filter applied
            type: str
            returned: when filter applied
        cloudera_runtime_version:
            description: CDP Private Cloud Base version filter applied
            type: str
            returned: when filter applied
        cloudera_data_services_version:
            description: CDP Private Cloud Data Services version filter applied
            type: str
            returned: when filter applied
        cloudera_flow_management_version:
            description: Cloudera Flow Management version filter applied
            type: str
            returned: when filter applied
        cloudera_streaming_analytics_version:
            description: Cloudera Streaming Analytics version filter applied
            type: str
            returned: when filter applied
        cloudera_data_visualization_version:
            description: Cloudera Data Visualization version filter applied
            type: str
            returned: when filter applied
        cds_spark_version:
            description: CDS Powered by Apache Spark version filter applied
            type: str
            returned: when filter applied
        python_version:
            description: Python version filter applied
            type: str
            returned: when filter applied
        operating_system:
            description: Operating system filter applied
            type: str
            returned: when filter applied
        jdk:
            description: JDK filter applied
            type: str
            returned: when filter applied
        database:
            description: Database filter applied
            type: str
            returned: when filter applied
        processor:
            description: Processor filter applied
            type: str
            returned: when filter applied
        kubernetes:
            description: Kubernetes filter applied
            type: str
            returned: when filter applied
api_url:
    description: The complete API URL that was called
    type: str
    returned: always
"""

import json
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_native


class ClouderaSupportMatrixInfo:
    """
    Class to handle Cloudera Support Matrix API interactions.
    
    This class manages the construction of API requests, filtering parameters,
    and processing of responses from the Cloudera Support Matrix API.
    """
    
    BASE_URL = "https://supportmatrix.cloudera.com/supportmatrices/cldr"
    
    # Mapping of parameter names to actual product names in the API
    PRODUCT_NAME_MAPPING = {
        'cloudera_manager_version': 'Cloudera Manager',
        'cloudera_runtime_version': 'CDP Private Cloud Base',
        'cloudera_data_services_version': 'CDP Private Cloud Data Services',
        'cloudera_flow_management_version': 'Cloudera Flow Management',
        'cloudera_streaming_analytics_version': 'Cloudera Streaming Analytics',
        'cloudera_data_visualization_version': 'Cloudera Data Visualization',
        'cds_spark_version': 'CDS Powered by Apache Spark',
        'python_version': 'Python',
    }
    
    def __init__(self, module):
        """
        Initialize the ClouderaSupportMatrixInfo class.
        
        Args:
            module: AnsibleModule instance
        """
        self.module = module
        
        # Extract product version parameters
        self.product_versions = {}
        for param_name in self.PRODUCT_NAME_MAPPING.keys():
            version = module.params.get(param_name)
            if version:
                self.product_versions[param_name] = version
        
        # Extract other filter parameters
        self.operating_system = module.params.get('operating_system')
        self.jdk = module.params.get('jdk')
        self.database = module.params.get('database')
        self.processor = module.params.get('processor')
        self.kubernetes = module.params.get('kubernetes')
        self.timeout = module.params.get('timeout', 30)
        self.validate_certs = module.params.get('validate_certs', True)
        
        # Initialize return values
        self.support_matrix_data = {}
        self.filters_applied = {}
        self.api_url = self.BASE_URL
    
    def _url_encode_spaces(self, text):
        """
        URL encode only the spaces in text, leaving other characters intact.
        
        Args:
            text: Text that may contain spaces
            
        Returns:
            str: Text with spaces encoded as %20
        """
        return text.replace(' ', '%20')
        
    def _build_query_conditions(self):
        """
        Build query conditions for API filtering.
        
        Returns:
            str: Query conditions string for the API request
        """
        conditions = []
        
        # Build operating system condition first (must come before PRODUCT)
        if self.operating_system:
            encoded_os = self._url_encode_spaces(self.operating_system)
            conditions.append(f"OPERATING_SYSTEM={encoded_os}")
            self.filters_applied['operating_system'] = self.operating_system
        
        # Build single PRODUCT condition with comma-separated values
        if self.product_versions:
            products = []
            for param_name, version in self.product_versions.items():
                product_name = self.PRODUCT_NAME_MAPPING[param_name]
                # URL encode spaces in both product name and version
                product_version_string = f"{product_name}-{version}"
                encoded_product_version = self._url_encode_spaces(product_version_string)
                products.append(encoded_product_version)
                self.filters_applied[param_name] = version
            
            if products:
                # Join products with commas for a single PRODUCT parameter
                product_condition = f"PRODUCT={','.join(products)}"
                conditions.append(product_condition)
            
        # Build JDK condition
        if self.jdk:
            conditions.append(f"JDK={self.jdk}")
            self.filters_applied['jdk'] = self.jdk
            
        # Build database condition
        if self.database:
            conditions.append(f"DATABASE={self.database}")
            self.filters_applied['database'] = self.database
            
        # Build processor condition - encode spaces here too  
        if self.processor:
            encoded_processor = self._url_encode_spaces(self.processor)
            conditions.append(f"PROCESSOR={encoded_processor}")
            self.filters_applied['processor'] = self.processor
            
        # Build kubernetes condition
        if self.kubernetes:
            conditions.append(f"KUBERNETES={self.kubernetes}")
            self.filters_applied['kubernetes'] = self.kubernetes
        
        return ";".join(conditions)
    
    def _build_api_url(self):
        """
        Build the complete API URL with query parameters.
        
        Returns:
            str: Complete API URL
        """
        conditions = self._build_query_conditions()
        
        if conditions:
            # Add trailing semicolon as shown in the curl example
            # Don't URL encode the entire condition string, only spaces are encoded
            self.api_url = f"{self.BASE_URL}?condition={conditions};"
        else:
            self.api_url = self.BASE_URL
            
        return self.api_url
    
    def fetch_support_matrix_data(self):
        """
        Fetch support matrix data from the Cloudera API using requests library.
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not HAS_REQUESTS:
            self.module.fail_json(
                msg="The requests library is required for this module. Install it with: pip install requests"
            )
            return False
            
        try:
            # Build the API URL
            api_url = self._build_api_url()
            
            # Prepare headers
            headers = {
                'Accept': '*/*',
                'Content-Type': 'application/json',
                'User-Agent': 'Ansible/cloudera.cluster'
            }
            
            # Make the API request using requests
            response = requests.get(
                api_url,
                headers=headers,
                timeout=self.timeout,
                verify=self.validate_certs
            )
            
            # Raise an exception for bad status codes
            response.raise_for_status()
            
            # Parse JSON response
            if response.text:
                try:
                    self.support_matrix_data = response.json()
                    
                except json.JSONDecodeError as e:
                    self.module.fail_json(
                        msg=f"Failed to parse JSON response: {to_native(e)}",
                        api_url=api_url,
                        response_text=response.text[:500]  # First 500 chars for debugging
                    )
                    return False
            else:
                self.module.fail_json(
                    msg="Empty response received from API",
                    api_url=api_url
                )
                return False
                
            return True
            
        except requests.exceptions.HTTPError as e:
            self.module.fail_json(
                msg=f"HTTP error occurred: {to_native(e)}",
                api_url=api_url,
                http_status=e.response.status_code if e.response else None,
                http_reason=str(e.response.reason) if e.response else None
            )
            return False
            
        except requests.exceptions.ConnectionError as e:
            self.module.fail_json(
                msg=f"Connection error occurred: {to_native(e)}",
                api_url=api_url
            )
            return False
            
        except requests.exceptions.Timeout as e:
            self.module.fail_json(
                msg=f"Request timeout occurred: {to_native(e)}",
                api_url=api_url,
                timeout=self.timeout
            )
            return False
            
        except requests.exceptions.RequestException as e:
            self.module.fail_json(
                msg=f"Request error occurred: {to_native(e)}",
                api_url=api_url
            )
            return False
            
        except Exception as e:
            self.module.fail_json(
                msg=f"Unexpected error occurred: {to_native(e)}",
                api_url=api_url
            )
            return False


def main():
    """
    Main function to execute the Ansible module.
    """
    # Define module arguments
    argument_spec = dict(
        cloudera_manager_version=dict(type='str', required=False),
        cloudera_runtime_version=dict(type='str', required=False),
        cloudera_data_services_version=dict(type='str', required=False),
        cloudera_flow_management_version=dict(type='str', required=False),
        cloudera_streaming_analytics_version=dict(type='str', required=False),
        cloudera_data_visualization_version=dict(type='str', required=False),
        cds_spark_version=dict(type='str', required=False),
        python_version=dict(type='str', required=False),
        operating_system=dict(type='str', required=False),
        jdk=dict(type='str', required=False),
        database=dict(type='str', required=False),
        processor=dict(type='str', required=False),
        kubernetes=dict(type='str', required=False),
        timeout=dict(type='int', default=30),
        validate_certs=dict(type='bool', default=True)
    )
    
    # Create module instance
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True
    )
    
    # Create support matrix info instance
    support_matrix = ClouderaSupportMatrixInfo(module)
    
    # Fetch support matrix data
    success = support_matrix.fetch_support_matrix_data()
    
    if success:
        # Prepare successful response
        result = dict(
            changed=False,
            support_matrix_data=support_matrix.support_matrix_data,
            filters_applied=support_matrix.filters_applied,
            api_url=support_matrix.api_url
        )
        
        module.exit_json(**result)
    else:
        # This should not be reached as errors are handled in fetch_support_matrix_data
        module.fail_json(msg="Unknown error occurred while fetching support matrix data")


if __name__ == "__main__":
    main() 