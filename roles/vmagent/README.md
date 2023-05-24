Role Name
=========

VMAgent deployment and configuration role.

Example Playbook
----------------

Example playbook with autoconf mode enabled.

```
- hosts: servers
  gather_facts: false

  roles:
    - role: vmagent
      vars:
        vmagent_remote_write_url: 'https://vmcluster-url/insert/0/prometheus/api/v1/write'
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
```

Testing
-------

```
molecule test --all --parallel
```

License
-------

gpl-3.0
