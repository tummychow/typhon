# Redmine

This role installs Redmine on an Arch Linux system with PostgreSQL as the database backend and nginx-passenger as the webserver. It's unlikely that you'll be able to use the role as-is for your own environment (unless your use case is literally the same as mine), but it has some nice features you should take advantage of if you are using Ansible to manage your own Redmine instance.

In particular this role is 100% idempotent (including Redmine rake tasks) and it uses bundler in deployment mode for reproducible installations. The role uses subversion to retrieve Redmine 2.5.2, no tarballs required.

To use the role you need some variables defined:

- `redmine.fulldir` for the place to unpack Redmine. This should be something like `/var/redmine-2.5`. Redmine will be checked out into this folder from the newest stable branch.
- `redmine.user`. The owner of the Redmine files is the same as the user that nginx's workers will run as. This matches up nicely with the behavior of passenger. If you were using Unicorn or Puma, you might want to fork this off into a variable of its own (and have Redmine's Ruby workers running as their own user, which would then be reverse proxied by nginx).
- `redmine.database`, `redmine.name` and `redmine.pass`. This is the Redmine database, plus its owner's name and password.
