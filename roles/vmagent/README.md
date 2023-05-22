Role Name
=========

VMAgent deployment and configuration role.

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: servers
      roles:
        - role: vmagent
          vars:
            vmagent_config_global_labels:
              env: 'nonprod'
              service: 'aparavi'
              component: 'platform'
            vmagent_auto_configure: true
            vmagent_auto_configure_labels:
              node_exporter:
                subcomponent: 'app'
              mysqld_exporter:
                subcomponent: 'db'
                service_instance: 'platform_eu'

Testing
-------

```
molecule test --all --parallel
```

License
-------

BSD

Author Information
------------------

An optional section for the role authors to include contact information, or a website (HTML is not allowed).
