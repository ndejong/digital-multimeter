# Usage

### Usage: dmm
```shell
Usage: dmm [OPTIONS] COMMAND [ARGS]...

  Digital multimeter CLI tool utilizing the DigitalMultimeter() module.

  Configuration can be achieved through command arguments, environment values
  or config file.

  Documentation available https://digital-multimeter.readthedocs.io

Options:
  -q, --quiet             Quiet mode; priority over --verbose
  -v, --verbose           Verbose logging; debug level.
  -W, --disable-warnings  Disable Python warnings.
  --version               Show the version and exit.
  --help                  Show this message and exit.

Commands:
  models  Provides a list of the supported digital multimeter models
  read    Read the digital multimeter and output data in various formats
```

### Usage: dmm read
```shell
Usage: dmm read [OPTIONS]

  Read the digital multimeter and output data in various formats

Options:
  -m, --model TEXT     DMM model; overrides env-variable and config.
  -c, --connect TEXT   DMM connection; overrides env-variable and config.
  -C, --config TEXT    Override config file; default=~/.digital-multimeter
  -n, --count INTEGER  Perform <count> readings; use 0 for non-stop.
  -o, --output TEXT    Output target file; default=stdout
  -f, --format TEXT    Output format json/csv; default=json
  --help               Show this message and exit.
```

### Usage: dmm models
```shell
Usage: dmm models [OPTIONS]

  Provides a list of the supported digital multimeter models

Options:
  -o, --output TEXT  Output target file; default=stdout
  -f, --format TEXT  Output format json/csv; default=json
  --help             Show this message and exit.
```
