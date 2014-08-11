# PostgreSQL

A role to install and configure postgres on Arch Linux. This is derived from [one](https://github.com/Ansibles/postgresql) of the most popular roles on Galaxy.

## Installation

Since this is Arch, I had to change some of the installation controls:

- use pacman instead of apt (well duh)
- use official packages for some python dependencies (psycopg2 and pycurl)
- remove the extensions. Not sure where these are in the Arch repositories but I know I don't use them.

## Configuration

The configuration, on the other hand, was mostly unmodified. I didn't touch any templates, but I still had to make some changes:

- unify data\_directory and conf\_directory. It looks like Debian distros store the postgres configs under /etc, while putting the database cluster under /var. However, Arch (and from what I gather, most other distributions) leave the configs in the same directory as the database cluster.
- replace the createcluster commands with initdb commands, and so on. Apparently the createcluster and dropcluster commands are Debian-specific as well. (I've never administrated a distro from the Debian family, so I wouldn't know, honestly.)
- split the cluster-building commands into their own task file and make them idempotent. The original role would recreate the cluster whenever you passed a `postgresql_cluster_reset` variable to Ansible. One unfortunate consequence was that the cluster would *never* get created unless you passed this variable at least once. I've reconfigured the cluster creation so that it only gets run if it can't find a cluster at the given target.
- clean up default variables for Arch - some things, like the socket directory and the data directory, had to be changed.
- consistent use of `on` and `off` as strings. The original default variables had a lot of cases where `on` and `off` were used without quotes. In YAML those are booleans. This results in some incorrect behavior, such as in `postgresql_synchronous_commit`. You might never get an error from postgres if those configuration options are being ignored, but that's still wrong. I've modified the default variables so that `on` and `off` are always quoted and treated as strings. This provides more predictable behavior and simplifies the templates.
- allow users to be set as a database owner by putting the `users` tasks before the `databases` tasks. Plus some minor tweaks to the database tasks to make that possible.

This role uses the standard PostgreSQL package *without modifications*. That means we also use the standard [systemd service](https://projects.archlinux.org/svntogit/packages.git/tree/trunk/postgresql.service?h=packages/postgresql), which expects the data directory will *always* be `/var/lib/postgres/data`. If you need to change this directory, you will probably need to set up your own service file as well.

## Other

Original role was under the MIT license, so this is also under MIT.

Remember to have your locales configured and generated before you use this role. Any nonexistent locales referenced in your configuration will raise errors when postgres tries to start.

## Future Improvements

Manage the systemd unit file for postgres. Right now Arch packages the service file as well. For whatever reason, our service file is quite dependent on the location of the data directory. I'm guessing this is because the server process needs to know where that directory is, right at startup, so there's no way to separate the service file from the configuration for the data directory. If that is the case, then the service file should also be part of this Ansible role, as a template.
