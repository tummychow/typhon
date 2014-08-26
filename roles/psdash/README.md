# psdash

This role installs psdash on an Arch Linux system. The role is notable for using Phusion Passenger. From what I gather, passenger is not the most popular of options for python deployment. It doesn't benefit from the popularity it has for Rubyists. Nevertheless, I'm already using passenger so I don't want to bring in another application server (eg uWSGI). It's not that hard to set up python applications on passenger either, although there is precious little information about how to do so.

To use the role you need some variables defined:

- `psdash.fulldir` for the place to unpack psdash. These should be something like `/var/psdash-0.4.0`.
- `psdash.user`. The owner of the psdash files is the same as the user that nginx's workers will run as. This matches up nicely with the behavior of passenger.

The role installs psdash from pip, inside a virtualenv. Passenger is then configured to use the virtualenv's python, rather than the global one. I've provided the `passenger_wsgi.py` that teaches Passenger how to serve this application. If you are serving other Flask applications, you might want to take a look at this `passenger_wsgi.py` as a guideline for your own stuff.

Note that passenger will never run its worker processes as root. If you try to set `passenger_user` to root, it gets demoted to `nobody` for security. Therefore, if you run psdash under passenger, it can only inspect processes and files that its user (in this case, `http`) has permission to read. Processes and files owned by more privileged users, like root, will be inacessible.
