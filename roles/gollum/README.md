# Gollum

This role installs Gollum with the repository under `./repo`. Gollum is quite easy to install; all you need is a Gemfile (with a Gemfile.lock for `bundler --deployment`) and a `config.ru`. Mine is nicely commented if you need some tips on what the options mean.

The role needs only two variables:

- `gollum.fulldir`, to indicate the path you want Gollum to live under. In my case that's `/var/gollum`.
- `gollum.user`. As with Redmine, the Gollum stuff will be owned by the same user that nginx (and passenger) are running under. If you want to run the application workers under another user, you should probably parameterize this as a separate variable.
