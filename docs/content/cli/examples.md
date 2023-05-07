# Examples

### Example 1: `dmm read`
Obtain a single reading from the `Default` multimeter attached to `/dev/ttyUSB0` in JSON 
format.

```shell
user@computer:~$ dmm read --connect /dev/ttyUSB0 
{
  "reading": {
    "value": 156.70000000000002,
    "unit_name": "volts",
    "unit_symbol": "V",
    "scale": 0.001,
    "scale_name": "milli",
    "scale_symbol": "m",
    "scaled_value": 0.15670000000000003,
    "is_relative": false
  },
  "instrument": {
    "module": "MultimeterDigitechQM1538",
    "operation_mode": "voltage_dc",
    "low_battery": false,
    "is_hold": false
  },
  "time": {
    "elapsed": 0.349347334,
    "interval": 0.349347334,
    "timestamp": 1605936374.7694516,
    "unit_name": "second",
    "unit_symbol": "s"
  }
}
```


### Example 2 `dmm read` with CSV output and 5x readings
Obtain 5x readings from a TekPower_TP4000ZC multimeter attached to `/dev/ttyUSB0` in CSV 
format.

```shell
user@computer:~$ dmm read --connect /dev/ttyUSB0 --model TekPower_TP4000ZC -n 5 -f csv 
reading_value,reading_unit_name,reading_unit_symbol,reading_scale,reading_scale_name,reading_scale_symbol,reading_scaled_value,reading_is_relative,instrument_module,instrument_operation_mode,instrument_low_battery,instrument_is_hold,time_elapsed,time_interval,time_timestamp,time_unit_name,time_unit_symbol
173.0,volts,V,0.001,milli,m,0.17300000000000001,False,MultimeterDigitechQM1538,voltage_dc,False,False,0.181438965,0.181438965,1605958015.0846217,second,s
172.70000000000002,volts,V,0.001,milli,m,0.17270000000000002,False,MultimeterDigitechQM1538,voltage_dc,False,False,0.531427706,0.34998874100000005,1605958015.4346104,second,s
172.5,volts,V,0.001,milli,m,0.17250000000000001,False,MultimeterDigitechQM1538,voltage_dc,False,False,0.881454916,0.35002721000000003,1605958015.7846375,second,s
172.4,volts,V,0.001,milli,m,0.1724,False,MultimeterDigitechQM1538,voltage_dc,False,False,1.231092399,0.349637483,1605958016.1342752,second,s
172.3,volts,V,0.001,milli,m,0.1723,False,MultimeterDigitechQM1538,voltage_dc,False,False,1.581224202,0.350131803,1605958016.484407,second,s
```


### Example 3: `dmm read` with CSV output using environment variables
Obtain a single reading from a Tecpel_DMM8062 multimeter attached to `/dev/ttyUSB0` using 
environment variable settings and show verbose debug logs.

```shell
user@computer:~$ export DMM_MODEL="Tecpel_DMM8062"
user@computer:~$ export DMM_CONNECT="/dev/ttyUSB0"
user@computer:~$ dmm -v read -f csv
[DEBUG|2020-11-22 12:52:58,023|digital_multimeter.cli.config]: "model" returned from environment variable: DMM_MODEL
[DEBUG|2020-11-22 12:52:58,023|digital_multimeter.cli.config]: "connect" returned from environment variable: DMM_CONNECT
[DEBUG|2020-11-22 12:52:58,023|digital_multimeter.cli.click]: model=Tecpel_DMM8062
[DEBUG|2020-11-22 12:52:58,023|digital_multimeter.cli.click]: connect=/dev/ttyUSB0
[DEBUG|2020-11-22 12:52:58,023|digital_multimeter.DigitalMultimeter]: Digital multimeter model: Tecpel_DMM8062
[DEBUG|2020-11-22 12:52:58,023|digital_multimeter.DigitalMultimeter]: Loading digital multimeter class: MultimeterFortuneFS9721
[DEBUG|2020-11-22 12:52:58,029|digital_multimeter.multimeters.MultimeterFortuneFS9721]: Serial connection okay: /dev/ttyUSB0
[DEBUG|2020-11-22 12:52:58,417|digital_multimeter.multimeters.MultimeterFortuneFS9721]: Received complete packet with 14x nibbles
reading_value,reading_unit_name,reading_unit_symbol,reading_scale,reading_scale_name,reading_scale_symbol,reading_scaled_value,reading_is_relative,instrument_module,instrument_operation_mode,instrument_low_battery,instrument_is_hold,time_elapsed,time_interval,time_timestamp,time_unit_name,time_unit_symbol
124.5,volts,V,0.001,milli,m,0.1245,False,MultimeterFortuneFS9721,voltage_dc,False,False,0.38927618,0.38927618,1606013578.4175675,second,s
[DEBUG|2020-11-22 12:52:58,417|digital_multimeter.cli.click]: Readings cycle count: 1
[DEBUG|2020-11-22 12:52:58,418|digital_multimeter.multimeters.MultimeterFortuneFS9721]: Closing serial connection
```


### Example 4: `dmm read` using configuration file
Obtain a single reading from a Tecpel_DMM8062 multimeter attached to `/dev/ttyUSB0` using 
settings provided in a configuration file.

NB: by default any configuration file located at `~/.digital-multimeter` will be loaded 
unless overridden at the command line as shown in this example.

```shell
user@computer:~$ cat tests/digital_multimeter/.digital-multimeter
[digital-multimeter]
model = Tecpel_DMM8062
connect = /dev/ttyUSB0

user@computer:~$ dmm read --config tests/digital_multimeter/.digital-multimeter 
{
  "reading": {
    "value": 126.4,
    "unit_name": "volts",
    "unit_symbol": "V",
    "scale": 0.001,
    "scale_name": "milli",
    "scale_symbol": "m",
    "scaled_value": 0.1264,
    "is_relative": false
  },
  "instrument": {
    "module": "MultimeterFortuneFS9721",
    "operation_mode": "voltage_dc",
    "low_battery": false,
    "is_hold": false
  },
  "time": {
    "elapsed": 0.260465548,
    "interval": 0.260465548,
    "timestamp": 1606014052.9823334,
    "unit_name": "second",
    "unit_symbol": "s"
  }
}
```


### Example 5: `dmm read` to file
Provide verbose debug logging output while obtaining a reading from a Voltcraft_VC820 
multimeter attached to `/dev/ttyUSB0` and write output to file `/tmp/data`

```shell
user@computer:~$ dmm --verbose read --connect /dev/ttyUSB0 --model Voltcraft_VC820 --output /tmp/data
[DEBUG|2020-11-22 12:23:25,811|digital_multimeter.cli.config]: "model" unset because no configuration file found.
[DEBUG|2020-11-22 12:23:25,811|digital_multimeter.cli.config]: "connect" unset because no configuration file found.
[DEBUG|2020-11-22 12:23:25,811|digital_multimeter.cli.click]: model=Voltcraft_VC820
[DEBUG|2020-11-22 12:23:25,811|digital_multimeter.cli.click]: connect=/dev/ttyUSB0
[DEBUG|2020-11-22 12:23:25,811|digital_multimeter.DigitalMultimeter]: Digital multimeter model: Voltcraft_VC820
[DEBUG|2020-11-22 12:23:25,811|digital_multimeter.DigitalMultimeter]: Loading digital multimeter class: MultimeterFortuneFS9721
[DEBUG|2020-11-22 12:23:25,818|digital_multimeter.multimeters.MultimeterFortuneFS9721]: Serial connection okay: /dev/ttyUSB0
[DEBUG|2020-11-22 12:23:26,148|digital_multimeter.multimeters.MultimeterFortuneFS9721]: Received complete packet with 14x nibbles
[DEBUG|2020-11-22 12:23:26,149|digital_multimeter.cli.click]: Readings cycle count: 1
[DEBUG|2020-11-22 12:23:26,149|digital_multimeter.multimeters.MultimeterFortuneFS9721]: Closing serial connection
```


### Example 6: `dmm models`
List the supported digital multimeter models

```shell
user@computer:~$ dmm models
{
  "models": [
    "Default",
    "Digitec_DT9604",
    "Digitech_QM1538",
    "Digitek_DT4000ZC",
    "Editronic_EDI9604",
    "PCE_PCEDM32",
    "Tecpel_DMM8062",
    "TekPower_TP4000ZC",
    "UniTrend_UT30A",
    "UniTrend_UT30E",
    "UniTrend_UT60E",
    "Voltcraft_VC820",
    "Voltcraft_VC840",
    "Voltcraft_VC870"
  ]
}
```
