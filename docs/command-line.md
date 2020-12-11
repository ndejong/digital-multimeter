# Digital Multimeter

## Command Line
Usage for sub-commands can easily be obtained using the `--help` switch after the sub-command.

Refer to the [Usage](./usage) and [Examples](./examples) for more detail.

## Environment Variables
* `DMM_MODEL` - the digital multimeter model to use for the connection protocol.
* `DMM_CONNECT` - the digital multimeter connection device to use, for example `/dev/ttyUSB0`.

For example, setting the model as an environment variable:-
```shell
user@computer:~$ export DMM_MODEL=Digitech_QM1538
```

## Configuration File
A configuration file will be read from any location specified using the `--config` option.  If this option is not
set an attempt to locate read a configuration from `~/.digital-multimeter` and finally from
`/etc/digital-multimeter` will be made.  Use the `--verbose` to review which file is being read if there is any
confusion.

Settings provided in configuration files always override the equivalent environment value settings.

The configuration file is standard [config](https://docs.python.org/3/library/configparser.html) file format and 
requires a `[digital-multimeter]` section as shown in the sample.

Sample configuration file:- 
```ini
[digital-multimeter]
model = Tecpel_DMM8062
connect = /dev/ttyUSB0
```
