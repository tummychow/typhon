# Redmine

This role installs Redmine on an Arch Linux system with PostgreSQL as the database backend and nginx-passenger as the webserver. It's unlikely that you'll be able to use the role as-is for your own environment (unless your use case is literally the same as mine), but it has some nice features you should take advantage of if you are using Ansible to manage your own Redmine instance.

In particular this role is 100% idempotent (including Redmine rake tasks) and it uses bundler in deployment mode for reproducible installations. You need the Redmine 2.5.2 [tarball](http://www.redmine.org/releases/redmine-2.5.2.tar.gz) from Redmine's download page (put it in `roles/redmine/files`) before the role will actually work. In the future I might adapt the role to use svn instead of a tarball.

To use the role you need some variables defined:

- `redmine.dir` and `redmine.fulldir` for the place to unpack Redmine. These should be something like `/var` (the place to unarchive Redmine) and `/var/redmine-2.5.2` (the place where Redmine actually ends up once it's unpacked).
- `nginx_user`. The owner of the Redmine files is the same as the user that nginx's workers will run as. This matches up nicely with the behavior of passenger. If you were using Unicorn or Puma, you might want to fork this off into a variable of its own (and have Redmine's Ruby workers running as their own user, which would then be reverse proxied by nginx).
- `redmine.database`, `redmine.name` and `redmine.pass`. This is the Redmine database, plus its owner's name and password.
