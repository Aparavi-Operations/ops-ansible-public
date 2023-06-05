Atop Ansible role
=================

Installs and configures Atop https://www.atoptool.nl


Example Playbook
----------------

    - hosts: servers
      roles:
         - { role: atop, atop_interval_seconds: 60 }

Testing
-------

```
molecule test --all --parallel
```

License
-------

gpl-3.0
