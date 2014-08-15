# An Ansible Playbook

An Ansible playbook to install some stuff. The target is an Arch Linux system with the `base` and `base-devel` groups installed. The playbook will install:

- nginx-passenger as the main webserver
- postgresql
- [redmine](http://www.redmine.org) running on the postgresql backend
- [gollum](https://github.com/gollum/gollum)
- [psdash](https://github.com/jahaja/psdash)

## Steps

1. change hosts.ini to contain your hosts as needed.
2. get the various tarballs you need to actually run the playbook (mainly a tarball for nginx-passenger). See the READMEs under each role for more information.
3. run ansible-playbook on the target

## License

My own stuff is under BSD 3-clause. If I modified an existing role that someone else wrote, then my version is under the same license as theirs.
