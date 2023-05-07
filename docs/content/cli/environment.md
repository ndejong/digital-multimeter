# Environment Variables

The following environment variables can be set:-

* `DMM_MODEL` - the digital multimeter model to use for the connection protocol.
* `DMM_CONNECT` - the digital multimeter connection device to use, for example `/dev/ttyUSB0`.

These provide a way to define the `--model` and `--connect` CLI arguments without having to 
supply them each time.

For example, setting the model as an environment variable:-
```shell
user@computer:~$ export DMM_MODEL=Digitech_QM1538
```
