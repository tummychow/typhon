# nginx

This role is derived from [another nginx role](https://github.com/bennojoy/nginx) by Benno Joy. It's really good. Just look at his nginx configuration template if you don't believe me.

## Installation

To install the actual package, I use an AUR tarball that you can find [here](https://aur.archlinux.org/packages/nginx-passenger). I've mirrored the tarball into this role [here](files/nginx-passenger), because you never know when AUR packages will disappear. The package updates fairly frequently to keep track of the currently released Passenger version, so sometimes the version in this repository may lag behind. **PSA for new Arch users: always read the PKGBUILD before installing, and do not install packages from untrusted sources. Use the AUR at your own risk.**

This role expects the package to be installable via pacman, so you have to build it first. The playbook does not do this for you, because building a package over and over again every time you run the playbook is wasteful and computationally expensive (especially on ARM single-board computers, where compiling passenger is painstainkingly slow). I haven't found a good way around that problem yet. I assume you are familiar with AUR packages and how you build and install them. If you aren't, then you really shouldn't be using AUR packages in the first place (read the PSA again).

Leave the tarball in the `nginx-passenger` directory. It should be at a path like `roles/nginx/files/nginx-passenger/nginx-passenger-1.6.0-4-x86_64.pkg.tar.xz`. That's where the role expects it to be located.

The tarball gets copied to the target system under `/root`, and then it gets installed from there. The playbook won't reinstall the package if it finds that the same tarball is already in the same place.

## Configuration

I have mostly preserved Benno Joy's awesome nginx configuration templates, because they're pretty great. The notes from his readme will also apply here. My changes are minor:

- removed the `user` directives that were specific to Debian and Red Hat. Those don't really apply to Arch, after all. Arch uses a user called `http` by default.
- removed the `pid` directive. This is specified by the systemd service file on Arch, and generally should be left alone.
- add support for `worker_rlimit_nofile` (this is a main-level-only directive).
- remove the `gzip` directives. I moved their configuration to the default vars.
- significant expansions to the default variables. I added defaults for gzip and SSL (note: you should generate a dhparam). I also added the passenger control directives.

One quick note if you aren't familiar with YAML - the words `on` and `off`, as unquoted values, are parsed as booleans. Then, when Jinja2 renders the template, those booleans will come out as `True` and `False` (the Python constants for booleans), which, for nginx, is definitely not what you wanted. Wrap `on` and `off` in quotes.

I drop the sites into `/etc/nginx/conf.d` because I don't *really* care where those config files end up. It's Ansible's problem, anyway. You might want to put them into `sites-available` or something like that.

## Other

My modifications to the original nginx role are under the same license as that role. (It's under the BSD license, but the original role doesn't say 2-clause or 3-clause. IANAL.)

You should be able to use this role for configuring nginx on... any system, really. I basically took the installation part out and tweaked the configuration bits a little. It should also be easy to add the installation tasks for any distribution of your choice, if you're reasonably familiar with Ansible.

## Future Improvements

Any key should be able to take a list and iterate over its contents, instead of requiring a single dictionary. For example, this:

```yaml
location1:
  name: /
  try_files: $uri /$uri/index.html @passenger
location2:
  name: "@passenger"
  passenger_enabled: "on"
```

should really look like this:

```yaml
location:
  - name: /
    try_files: $uri /$uri/index.html @passenger
  - name: "@passenger"
    passenger_enabled: "on"
```

A lot of other nginx directives can appear multiple times (especially `listen 80; listen 443 ssl;`) so this feature should be available for any directive.

Site config should be created in `/etc/nginx/sites-available` and then symlinked to `sites-enabled`, as is the de-facto standard.
