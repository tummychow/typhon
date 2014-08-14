# nginx

This role is inspired by another [nginx role](https://github.com/bennojoy/nginx) by Benno Joy. I have significantly improved on the templates used by his role, and of course my role installs nginx-passenger, and of course my role targets Arch Linux.

## Installation

To install the actual package, I use an AUR tarball that you can find [here](https://aur.archlinux.org/packages/nginx-passenger). I've mirrored the tarball into this role [here](files/nginx-passenger), because you never know when AUR packages will disappear. The package updates fairly frequently to keep track of the currently released Passenger version, so sometimes the version in this repository may lag behind. **PSA for new Arch users: always read the PKGBUILD before installing, and do not install packages from untrusted sources. Use the AUR at your own risk.**

This role expects the package to be installable via pacman, so you have to build it first. The playbook does not do this for you, because building a package over and over again every time you run the playbook is wasteful and computationally expensive (especially on ARM single-board computers, where compiling passenger is painstainkingly slow). I haven't found a good way around that problem yet. I assume you are familiar with AUR packages and how you build and install them. If you aren't, then you really shouldn't be using AUR packages in the first place (read the PSA again).

Leave the tarball in the `nginx-passenger` directory. It should be at a path like `roles/nginx/files/nginx-passenger/nginx-passenger-1.6.0-4-x86_64.pkg.tar.xz`. That's where the role expects it to be located.

The tarball gets copied to the target system under `/root`, and then it gets installed from there. The playbook won't reinstall the package if it finds that the same tarball is already in the same place.

## Configuration

After bumping into the limitations of Benno Joy's original templates one time too many, I eventually decided to make my own nginx configuration template. I'm pretty satisfied with what I accomplished. The template uses a pair of mutually recursive jinja2 macros, so that your YAML is structurally the same as your nginx configuration.

Let me show you an example. You can have YAML like this:

```yaml
nginx_conf:
  user: http
  http:
    sendfile: on
    include:
      - mime.types
      - sites-enabled/*
    server:
      - _name: foo
        server_name: foo.example.com
        root: /var/foo
      - _name: bar
        server_name: bar.example.com
        location:
          - _name: /
            root: /var/bar
            try_files: $uri $uri/index.html @passenger
          - _name: "@passenger"
            passenger_enabled: on
```

And you will get nginx configuration like this:

```nginxconf
http  {
    sendfile on;
    include mime.types;
    include sites-enabled/*;
    server foo {
        root /var/foo;
        server_name foo.example.com;

    }
    server bar {
        location / {
            root /var/bar;
            try_files $uri $uri/index.html @passenger;

        }
        location @passenger {
            passenger_enabled on;

        }
        server_name bar.example.com;

    }

}
user http;
```

By the way, that example is not fabricated. I literally dropped into the python console right now, compiled my template, loaded a YAML file and rendered the template with that YAML file. That example is *real*.

### Template Features

Essentially my template transforms arbitrary YAML into nginx configuration. The directives have the same names in YAML as they do in nginx. There are some notable bonus features:

- you can use `on` and `off` in YAML without quotes. The template will detect any instances of the python `True` and `False` singletons; it prints them into the configuration as `on` and `off` automatically.
- lists of directives are transformed into repeated instances of the same directive. You can see this with the `include` directive in the example. This is also useful for things like `listen 80; listen 443 ssl;`.
- indentation comes for free. I didn't indent that example by hand... the template actually does that for you. Ah, the wonders of recursion! (Sorry about the newlines before right curly braces. Haven't figured out where those are coming from yet.)
- to specify a deeper configuration scope (eg root -> `http` -> `server` -> `location`), just drop down into another YAML object. The root of `nginx_conf` corresponds to the root of your nginx configuration, so you can specify top-level directives like `error_log` and `events {}` just as easily as any others.
- specify named locations with a special variable, `_name`. Any YAML key that starts with an underscore will not be emitted into the nginx configuration. We can use these keys for special purposes. For example, the name of a location, `location <name> {}`, comes from that `_name` variable.

### Template Gotchas

Iteration order over python dicts is undefined. That's why the directives are in such a strange order (eg `user` comes after `http {}` in the above example). Be careful with directives like `log_format`, because these are order-dependent, and they have to appear before they are referenced by other directives.

You can't append to a YAML array. You either use it as-is, or redefine it all out. For example, the role's default variables will include `mime.types` and `sites-enabled/*`. If you define your own includes, you have to remember to add those default variables into the array as well, or they just won't show up.

### Site Management

This nginx role takes advantage of its upgraded templates to provide upgraded site management as well. Sites are entries under the `nginx_sites` array:

```yaml
nginx_sites:
 - _filename: default
   _enabled: true
   server:
      server_name: _
      listen:
        - 80 default
        - 443 ssl default
      return: 444
  - _filename: foo
    _enabled: false
    server:
      server_name: foo
      listen: 80
      root: "/var/foo/public"
      location:
        - _name: /
          try_files: $uri $uri/index.html @passenger
        - _name: "@passenger"
          passenger_enabled: on
```

As you can see, each entry in the sites array starts out with a top-level map. There are two special keys here:

- `_filename`. This indicates the file that the site config will be stored in. For example, the filename `default` gets stored under `sites-available/default.conf`.
- `_enabled`. This is a YAML boolean. If it's true, a symlink will be made from `sites-available` to `sites-enabled`. This role includes all the files under `sites-enabled` by default. Any sites that have `_enabled: true` will be served, and others will be ignored.

The rest of the keys are all the same as for the top-level configuration. In fact, we use the same template for all the configuration files.

## Other

My modifications to the original nginx role are under the same license as that role. (It's under the BSD license, but the original role doesn't say 2-clause or 3-clause. IANAL.)

You should be able to use this role for configuring nginx on... any system, really. I basically took the installation part out and tweaked the configuration bits a little. It should also be easy to add the installation tasks for any distribution of your choice, if you're reasonably familiar with Ansible.
