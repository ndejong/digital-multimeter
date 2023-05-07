import logging
import time

import serial
from serial import SerialException

from ..exceptions import MultimeterException
from ..multimeters.MultimeterBase import MultimeterBase

SERIAL_BAUD = 2400
SERIAL_PARITY = "N"
SERIAL_STOPBITS = 1
PACKET_RETRY_LIMIT = 3

logger = logging.getLogger(__name__)


class MultimeterEDI9604Exception(MultimeterException):
    pass


class MultimeterEDI9604(MultimeterBase):
    serial = None

    def __init__(self, connect):
        super().__init__()
        try:
            self.serial = serial.Serial(
                port=connect, baudrate=SERIAL_BAUD, parity=SERIAL_PARITY, stopbits=SERIAL_STOPBITS
            )
            CRLF = False
            iter = 0
            last = None
            while not CRLF and iter < 14:
                current = self.serial.read(size=1)

                if last == b"\r" and current == b"\n":
                    CRLF = True

                last = current
                iter += 1

        except SerialException as e:
            raise MultimeterException(e)
        logger.debug("Serial connection okay: {}".format(connect))

    def __del__(self):
        if self.serial:
            logger.debug("Closing serial connection")
            self.serial.close()

    def get_reading(self):
        return self.parse_packet(self.receive_packet())

    def parse_packet(self, packet):
        value = self._parse_packet_value(packet)
        scale, scale_name, scale_symbol = self._parse_packet_scale(packet)
        if value is None or scale is None:
            scaled_value = None
        else:
            scaled_value = value * scale
        unit_name, unit_symbol = self._parse_packet_units(packet)
        timestamp_this = time.time_ns()
        time_interval = int(timestamp_this - self.timestamp_previous)
        self.timestamp_previous = timestamp_this
        return {
            "reading": {
                "value": value,
                "unit_name": unit_name,
                "unit_symbol": unit_symbol,
                "scale": scale,
                "scale_name": scale_name,
                "scale_symbol": scale_symbol,
                "scaled_value": scaled_value,
                "scope": self._parse_packet_scope(packet),
                "is_relative": self._parse_packet_relative(packet),
                "is_autorange": self._parse_packet_autorange(packet),
            },
            "instrument": {
                "module": __name__.split(".")[-1],
                "operation_mode": self._parse_packet_operation_mode(packet),
                "low_battery": self._parse_packet_low_battery(packet),
                "is_hold": self._parse_packet_hold(packet),
            },
            "time": {
                "elapsed": (timestamp_this - self.timestamp_start) * 1e-9,
                "interval": time_interval * 1e-9,
                "timestamp": timestamp_this * 1e-9,
                "unit_name": "second",
                "unit_symbol": "s",
            },
        }

    def receive_packet(self, retries=0):
        return self.serial.read(size=14)

    def _parse_packet_value(self, packet):
        if packet[0] == 45:
            sign = -1
        else:
            sign = +1

        try:
            divider = 10 ** (4 - int(packet[6:7]))
            number = int(packet[1:5])
        except ValueError:
            return None

        return sign * number / divider

    def _parse_packet_scale(self, packet):
        if packet[9] & 0b10000000:
            scale = 1e-6
            scale_name = "micro"
            scale_symbol = "\u03BC"
        elif packet[9] & 0b1000000:
            scale = 1e-3
            scale_name = "milli"
            scale_symbol = "m"
        elif packet[9] & 0b100000:
            scale = 1e3
            scale_name = "kilo"
            scale_symbol = "k"
        elif packet[9] & 0b10000:
            scale = 1e6
            scale_name = "mega"
            scale_symbol = "M"
        elif packet[8] & 0b10:
            scale = 1e-9
            scale_name = "nano"
            scale_symbol = "n"
        else:
            scale = 1
            scale_name = None
            scale_symbol = None
        return scale, scale_name, scale_symbol

    def _parse_packet_units(self, packet):
        if packet[10] & 0b10000000:
            unit_name = "volts"
            unit_symbol = "V"
        elif packet[10] & 0b1000000:
            unit_name = "amps"
            unit_symbol = "A"
        elif packet[10] & 0b100000:
            unit_name = "ohms"
            unit_symbol = "\u03A9"
        elif packet[10] & 0b1000:
            unit_name = "hertz"
            unit_symbol = "Hz"
        elif packet[10] & 0b100:
            unit_name = "farads"
            unit_symbol = "F"
        elif packet[9] & 0b10:
            unit_name = "duty-cycle"
            unit_symbol = "%"
        elif packet[10] & 0b10:
            unit_name = "celsius"
            unit_symbol = "C"
        elif packet[10] & 0b1:
            unit_name = "fahrenheit"
            unit_symbol = "F"
        else:
            raise MultimeterEDI9604Exception("Unknown measurement units")
        return unit_name, unit_symbol

    def _parse_packet_relative(self, packet):
        if packet[7] & 0b100:
            return True
        return False

    def _parse_packet_autorange(self, packet):
        if packet[7] & 0b100000:
            return "AUTO"
        return "MANUAL"

    def _parse_packet_scope(self, packet):
        if packet[8] & 0b100000:
            return "MAX"
        elif packet[8] & 0b10000:
            return "MIN"
        return "VALUE"

    def _parse_packet_operation_mode(self, packet):
        if packet[10] & 0b100000000 and packet[7] & 0b10000:
            return "voltage_dc"
        elif packet[10] & 0b100000000 and packet[7] & 0b1000:
            return "voltage_ac"
        elif packet[10] & 0b100000000 and packet[9] & 0b100:
            return "diode"
        elif packet[10] & 0b10000000 and packet[7] & 0b10000:
            return "current_dc"
        elif packet[10] & 0b10000000 and packet[7] & 0b1000:
            return "current_ac"
        elif packet[10] & 0b100000 and not packet[9] & 0b1000:
            return "resistance"
        elif packet[10] & 0b100000 and packet[9] & 0b1000:
            return "continuity"
        elif packet[10] & 0b1000:
            return "frequency"
        elif packet[10] & 0b100:
            return "capacitance"
        elif packet[10] & 0b10 or packet[10] & 0b1:
            return "temperature"
        raise MultimeterEDI9604Exception("Unsupported digital multimeter mode from packet")

    def _parse_packet_low_battery(self, packet):
        return False

    def _parse_packet_hold(self, packet):
        return False
