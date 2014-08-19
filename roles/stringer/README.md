# stringer

This role installs stringer on Arch Linux with a PostgreSQL backend. The [official stringer install guide](https://github.com/swanson/stringer/blob/master/docs/VPS.md) for bare metal hardware is a bit out of place in my environment:

- stringer's Gemfile fixes the ruby version to 2.0.0. This is a real pain on Arch where packages move forward frequently. The maintenance overhead of using a custom fixed-version ruby is not outrageous, but too much to be worth considering for my applications. We just have to yank the Gemfile's ruby directive out, which is a bit of a pain.
- stringer uses unicorn and the time-honored technique of reverse proxying to serve itself. Since we already have an nginx-passenger instance with a few ruby apps living on it, it would be nice to reuse that infrastructure. Thankfully, Rack has a standard deployment process so this is hardly even an issue.
- stringer is a 12-factor app, so it uses environment variables for database and session configuration. We'd like to move those into files that we can control via Ansible templates. We can configure the variables from nginx configuration via [`passenger_set_cgi_param`](https://www.phusionpassenger.com/documentation/Users%20guide%20Nginx.html#passenger_set_cgi_param). If you need to host 12-factor apps on passenger, this is the best way to do it.
- stringer uses cron to execute a rake task that updates the feeds. I would rather use a systemd timer, so that's what I did.

The role shares a lot of similarity with my Redmine role (stringer is not a Rails app, but it does use ActiveRecord). It has idempotent rake tasks, bundler in deployment mode, git-based deployment, etc. Note that stringer doesn't use tagged releases, so I fix the git revision to an exact SHA1. This is not convenient, but it's better than leaving the revision flying in the wind, where it can change unpredictably between installs.

The variables needed by this role are:

- `stringer.fulldir` for the place to unpack stringer. This should be something like `/var/stringer`. Stringer will be cloned into this folder from a fixed commit (update the commit yourself to keep up with newer versions of stringer).
- `stringer.user`. The owner of the stringer files is the same as the user that nginx's workers will run as. This matches up nicely with the behavior of passenger. If you were using Unicorn or Puma, you might want to fork this off into a variable of its own (and have Redmine's Ruby workers running as their own user, which would then be reverse proxied by nginx).
- `stringer.database`, `stringer.name` and `stringer.pass`. This is the stringer database, plus its owner's name and password.
- `stringer.frequency`. The frequency with which stringer will run its `fetch_feeds` rake task. For syntax, see [`systemd.time(5)`](http://www.freedesktop.org/software/systemd/man/systemd.time.html). I recommend something between `6h` and `12h`, depending on how obsessively you check your feeds.
- `stringer.token`. The session secret token for stringer. Unfortunately stringer doesn't generate this via rake task like Redmine does. Generate it with a command like `openssl rand -hex 40`.

## Using systemd timers

You might not be familiar with administrating systemd timers if all your past experience is on cron. I had experience with neither prior to working with stringer, so I recommend you read [this](https://wiki.archlinux.org/index.php/Systemd/cron_functionality).

This will list all the active timers on the system, including your stringer timer. You can see here when it's going to activate next, how much longer until then, when it last activated, and how long ago that was.

```bash
$ systemctl list-timers
NEXT                         LEFT       LAST                         PASSED       UNIT                         ACTIVATES
Tue 2014-08-19 11:37:47 EDT  11h left   Mon 2014-08-18 23:37:47 EDT  18s ago      stringer-fetch-feeds.timer   stringer-fetch-feeds.service
```

To inspect the timer itself, use status. `active (waiting)` means that the timer is counting down to its next trigger. If it's `active (elapsed)`, that means the timer is not counting down and it will never trigger. This usually means you configured the times wrong. (My systemd timer shouldn't do that, but if you do have an issue, please report it.)

```bash
$ systemctl status stringer-fetch-feeds.timer
● stringer-fetch-feeds.timer - stringer fetch_feeds timer
   Loaded: loaded (/etc/systemd/system/stringer-fetch-feeds.timer; enabled)
   Active: active (waiting) since Mon 2014-08-18 23:32:25 EDT; 2min 0s ago
```

Finally you can inspect the service itself as well. Most of the time it will be `inactive` because it's waiting to be triggered by the timer.

```bash
$ systemctl status stringer-fetch-feeds.service
● stringer-fetch-feeds.service - stringer fetch_feeds rake task
   Loaded: loaded (/etc/systemd/system/stringer-fetch-feeds.service; static)
   Active: inactive (dead) since Mon 2014-08-18 23:32:27 EDT; 5min ago
 Main PID: 15717 (code=exited, status=0/SUCCESS)
```

If you catch it in the act, you can see more interesting details:

```bash
$ systemctl status stringer-fetch-feeds.service
● stringer-fetch-feeds.service - stringer fetch_feeds rake task
   Loaded: loaded (/etc/systemd/system/stringer-fetch-feeds.service; static)
   Active: activating (start) since Mon 2014-08-18 23:37:47 EDT; 11ms ago
 Main PID: 15796 (bundle)
   CGroup: /system.slice/stringer-fetch-feeds.service
           └─15796 /usr/bin/ruby /usr/bin/bundle exec rake fetch_feeds
```
