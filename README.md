# foursquare-swarm-ical

[![PyPI Python Version badge](https://img.shields.io/pypi/pyversions/foursquare-swarm-ical)](https://pypi.org/project/foursquare-swarm-ical/)
[![PyPI Version badge](https://img.shields.io/pypi/v/foursquare-swarm-ical)](https://pypi.org/project/foursquare-swarm-ical/)
![License badge](https://img.shields.io/github/license/liskin/foursquare-swarm-ical)

## Overview

foursquare-swarm-ical is a …

<!-- FIXME: example image -->

## Installation

Using [pipx][]:

```
pipx ensurepath
pipx install foursquare-swarm-ical
```

To keep a local git clone around:

```
git clone https://github.com/liskin/foursquare-swarm-ical
make -C foursquare-swarm-ical pipx
```

Alternatively, if you don't need the isolated virtualenv that [pipx][]
provides, feel free to just:

```
pip install foursquare-swarm-ical
```

[pipx]: https://github.com/pypa/pipx

## Usage

<!-- include tests/readme/help.md -->
    $ foursquare-swarm-ical --help
    Usage: foursquare-swarm-ical [OPTIONS]
    
    Options:
      --config FILE    Read configuration from FILE.  [default:
                       /home/user/.config/foursquare_swarm_ical/config.yaml]
      --config-sample  Show sample configuration file
      --help           Show this message and exit.
<!-- end include tests/readme/help.md -->

<!-- FIXME: example -->

### Configuration file

Secrets (and other options) can be set permanently in a config file,
which is located at `~/.config/foursquare_swarm_ical/config.yaml` by default
(on Linux; on other platforms see output of `--help`).

Sample config file can be generated using the `--config-sample` flag:

<!-- include tests/readme/config-sample.md -->
    $ foursquare-swarm-ical --config-sample
<!-- end include tests/readme/config-sample.md -->

## Contributing

### Code

We welcome bug fixes, (reasonable) new features, documentation improvements,
and more. Submit these as GitHub pull requests. Use GitHub issues to report
bugs and discuss non-trivial code improvements; alternatively, get in touch
via [IRC/Matrix/Fediverse](https://work.lisk.in/contact/).

See [CONTRIBUTING.md](CONTRIBUTING.md) for more details about the code base
(including running tests locally).

Note that this project was born out of a desire to solve a problem I was
facing. While I'm excited to share it with the world, keep in mind that I'll
be prioritizing features and bug fixes that align with my personal use cases.
There may be times when I'm busy with other commitments and replies to
contributions might be delayed, or even occasionally missed. Progress may come
in bursts. Adjust your expectations accordingly.

### Donations (♥ = €)

If you like this tool and wish to support its development and maintenance,
please consider [a small donation](https://www.paypal.me/lisknisi/10EUR) or
[recurrent support through GitHub Sponsors](https://github.com/sponsors/liskin).

By donating, you'll also support the development of my other projects. You
might like these:

* <!-- FIXME: [name](link) --> – <!-- FIXME: description -->
