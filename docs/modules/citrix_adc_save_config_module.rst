:orphan:

.. _citrix_adc_save_config_module:

citrix_adc_save_config - Save Netscaler configuration.
++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.4.0

.. contents::
   :local:
   :depth: 2

Synopsis
--------
- This module uncoditionally saves the configuration on the target netscaler node.
- This module does not support check mode.
- This module is intended to run either on the ansible  control node or a bastion (jumpserver) with access to the actual netscaler instance.



Requirements
~~~~~~~~~~~~
The below requirements are needed on the host that executes this module.

- nitro python sdk


Parameters
----------

.. list-table::
    :widths: 10 10 60
    :header-rows: 1

    * - Parameter
      - Choices/Defaults
      - Comment
    * - nitro_pass
      -
      - The password with which to authenticate to the netscaler node.
    * - nitro_protocol
      - Choices:

          - http (*default*)
          - https
      - Which protocol to use when accessing the nitro API objects.
    * - nitro_timeout
      - Default:

        *310*
      - Time in seconds until a timeout error is thrown when establishing a new session with Netscaler.
    * - nitro_user
      -
      - The username with which to authenticate to the netscaler node.
    * - nsip
      -
      - The ip address of the netscaler appliance where the nitro API calls will be made.

        The port can be specified with the colon (:). E.g. ``192.168.1.1:555``.
    * - validate_certs
      - Default:

        *yes*
      - If ``no``, SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates.



Examples
--------

.. code-block:: yaml+jinja
    
    ---
    - name: Save netscaler configuration
      delegate_to: localhost
      citrix_adc_save_config:
        nsip: 172.18.0.2
        nitro_user: nsroot
        nitro_pass: nsroot
    
    - name: Setup server without saving  configuration
      delegate_to: localhost
      notify: Save configuration
      citrix_adc_server:
        nsip: 172.18.0.2
        nitro_user: nsroot
        nitro_pass: nsroot
    
        save_config: no
    
        name: server-1
        ipaddress: 192.168.1.1
    
    # Under playbook's handlers
    
    - name: Save configuration
      delegate_to: localhost
      citrix_adc_save_config:
        nsip: 172.18.0.2
        nitro_user: nsroot
        nitro_pass: nsroot


Return Values
-------------
.. list-table::
    :widths: 10 10 60
    :header-rows: 1

    * - Key
      - Returned
      - Description
    * - loglines

        *(list)*
      - always
      - list of logged messages by the module

        **Sample:**

        ['message 1', 'message 2']
    * - msg

        *(str)*
      - failure
      - Message detailing the failure reason

        **Sample:**

        Action does not exist