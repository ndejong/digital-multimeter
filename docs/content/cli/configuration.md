# Configuration File

A configuration file is relatively short and simple can be specified using the `--config` option.

If the `--config` option is not set, then an attempt to find a configuration file at the following 
path locations occurs:-

* `~/.digital-multimeter`
* `/etc/digital-multimeter`

Use the `--verbose` CLI switch to examine which config file is being read.

Settings provided in configuration files always override their equivalent environment
value settings.

The configuration file is standard [config](https://docs.python.org/3/library/configparser.html) file 
format and requires a `[digital-multimeter]` section as shown in the sample.

Sample configuration file:- 
```ini
[digital-multimeter]
model = Tecpel_DMM8062
connect = /dev/ttyUSB0
```
