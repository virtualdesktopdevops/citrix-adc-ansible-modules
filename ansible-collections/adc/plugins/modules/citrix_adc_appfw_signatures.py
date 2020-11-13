#!/usr/bin/python
# -*- coding: utf-8 -*-

#  Copyright (c) 2018 Citrix Systems
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: citrix_adc_appfw_signatures
short_description: Configuration for configured confidential form fields resource.
description: Configuration for configured confidential form fields resource.

version_added: "1.0.0"

author:
    - George Nikolopoulos (@giorgos-nikolopoulos)
    - Sumanth Lingappa (@sumanth-lingappa)

options:

    name:
        description:
            - "Name of the signature object."
            - "Minimum length =  1"
            - "Maximum length =  31"
        type: str

    src:
        description:
            - >-
                URL (protocol, host, path, and file name) for the location at which to store the imported signatures
            - >-
                NOTE: The import fails if the object to be imported is on an HTTPS server that requires client
                authentication for access.
            - "Minimum length =  1"
            - "Maximum length =  2047"
        type: str

    xslt:
        description:
            - "XSLT file source."
            - "Maximum length =  2047"
        type: str

    comment:
        description:
            - "Any comments to preserve information about the signatures object."
            - "Maximum length =  128"
        type: str

    overwrite:
        description:
            - "Overwrite any existing signatures object of the same name."
        type: bool

    merge:
        description:
            - "Merges the existing Signature with new signature rules."
        type: bool

    preservedefactions:
        description:
            - "preserves def actions of signature rules."
        type: bool

    sha1:
        description:
            - "File path for sha1 file to validate signature file."
            - "Minimum length =  1"
            - "Maximum length =  2047"
        type: str

    mergedefault:
        description:
            - "Merges signature file with default signature file."
        type: bool


extends_documentation_fragment: citrix.adc.citrixadc
'''

EXAMPLES = '''
- hosts: citrix_adc

  gather_facts: False
  tasks:
    - name: Setup confidential field id
      delegate_to: localhost
      citrix_adc_appfw_signatures:
        nitro_user: nsroot
        nitro_pass: nsroot
        nsip: 192.168.1.2
        state: present
        fieldname: signatures_integration_test
        url: 'HTTP.REQ.HOSTNAME.DOMAIN.EQ("blog.example.com")'
        isregex: REGEX
        comment: 'conf id field comment'
'''

RETURN = '''
loglines:
    description: list of logged messages by the module
    returned: always
    type: list
    sample: ['message 1', 'message 2']

msg:
    description: Message detailing the failure reason
    returned: failure
    type: str
    sample: "Action does not exist"
'''

import copy

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.citrix.adc.plugins.module_utils.citrix_adc import (
    NitroResourceConfig,
    NitroException,
    netscaler_common_arguments,
    log,
    loglines
)


class ModuleExecutor(object):

    def __init__(self, module):
        self.module = module
        self.main_nitro_class = 'appfwsignatures'

        # Dictionary containing attribute information
        # for each NITRO object utilized by this module
        self.attibute_config = {
            'appfwsignatures': {
                'attributes_list': [
                    'name',
                    'src',
                    'xslt',
                    'comment',
                    'overwrite',
                    'merge',
                    'preservedefactions',
                    'sha1',
                    'mergedefault',
                ],
                'transforms': {
                },
                'get_id_attributes': [
                    'name',
                ],
                'delete_id_attributes': [
                    'name',
                ],
            },

        }

        self.module_result = dict(
            changed=False,
            failed=False,
            loglines=loglines,
        )

    def main_object_exists(self, config):
        try:
            main_object_exists = config.exists(get_id_attributes=self.attibute_config[self.main_nitro_class]['get_id_attributes'])
        except NitroException as e:
            if e.errorcode == 3380 or e.errorcode == 3187:
                # errorcode 3380: "Signature does not exist" NS12.1
                # errorcode 3187: "Imported file does not exist" in NS11.1 and NS12.0
                return False
            else:
                raise

        return main_object_exists

    def get_main_config(self):
        manipulated_values_dict = copy.deepcopy(self.module.params)

        # We do not want the state module param to be interpreted as the appfwsignatures parameter value
        if 'state' in manipulated_values_dict:
            del manipulated_values_dict['state']

        config = NitroResourceConfig(
            module=self.module,
            resource=self.main_nitro_class,
            attribute_values_dict=manipulated_values_dict,
            attributes_list=self.attibute_config[self.main_nitro_class]['attributes_list'],
            transforms=self.attibute_config[self.main_nitro_class]['transforms'],
        )

        return config

    def import_and_update(self):
        # check if main object exists
        config = self.get_main_config()

        if not self.main_object_exists(config):
            self.module_result['changed'] = True
            if not self.module.check_mode:
                config.import_object()
                config.update_object()

    def delete(self):
        # Check if main object exists
        config = self.get_main_config()

        if self.main_object_exists(config):
            self.module_result['changed'] = True
            if not self.module.check_mode:
                config.delete(delete_id_attributes=self.attibute_config[self.main_nitro_class]['delete_id_attributes'])

    def main(self):
        try:

            if self.module.params['state'] == 'present':
                self.import_and_update()
            elif self.module.params['state'] == 'absent':
                self.delete()

            self.module.exit_json(**self.module_result)

        except NitroException as e:
            msg = "nitro exception errorcode=%s, message=%s, severity=%s" % (str(e.errorcode), e.message, e.severity)
            self.module.fail_json(msg=msg, **self.module_result)
        except Exception as e:
            msg = 'Exception %s: %s' % (type(e), str(e))
            self.module.fail_json(msg=msg, **self.module_result)


def main():

    argument_spec = dict()

    module_specific_arguments = dict(
        name=dict(type='str'),
        src=dict(type='str'),
        xslt=dict(type='str'),
        comment=dict(type='str'),
        overwrite=dict(type='bool'),
        merge=dict(type='bool'),
        preservedefactions=dict(type='bool'),
        sha1=dict(type='str'),
        mergedefault=dict(type='bool'),

    )

    argument_spec.update(netscaler_common_arguments)
    argument_spec.update(module_specific_arguments)

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    executor = ModuleExecutor(module=module)
    executor.main()


if __name__ == '__main__':
    main()
