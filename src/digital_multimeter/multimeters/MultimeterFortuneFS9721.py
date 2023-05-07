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


class MultimeterFortuneFS9721Exception(MultimeterException):
    pass


class MultimeterFortuneFS9721(MultimeterBase):
    serial = None

    def __init__(self, connect):
        super().__init__()
        try:
            self.serial = serial.Serial(
                port=connect, baudrate=SERIAL_BAUD, parity=SERIAL_PARITY, stopbits=SERIAL_STOPBITS
            )
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
        value = self._parse_packet_display_value(packet)
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
                "is_relative": self._parse_packet_relative(packet),
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
        packet = []
        byte = None
        byte_index = 0
        while byte_index != 1:
            byte = self.serial.read(size=1)
            byte_index = self._byte_index(byte)
        packet.append(self._byte_nibble(byte))

        byte_index_expect = 2
        while len(packet) < 14:
            byte = self.serial.read(size=1)
            if self._byte_index(byte) == byte_index_expect:
                packet.append(self._byte_nibble(byte))
            else:
                if retries >= PACKET_RETRY_LIMIT:
                    raise MultimeterFortuneFS9721Exception(
                        "Received out of order bytes " "after {} retries".format(PACKET_RETRY_LIMIT)
                    )
                logger.debug("Received out of order packet data, retrying")
                return self.receive_packet(retries=retries + 1)
            byte_index_expect += 1
        logger.debug("Received complete packet with 14x nibbles")
        return packet

    def _byte_index(self, byte):
        binary_string = "{:08b}".format(int(byte.hex(), 16))[0:4]
        return int(binary_string, 2)

    def _byte_nibble(self, data):
        return "{:08b}".format(int(data.hex(), 16))[-4:]

    def _parse_packet_operation_mode(self, packet):
        if int(packet[12][0]) == 1 and int(packet[0][0]) == 1:
            return "current_ac"
        elif int(packet[12][0]) == 1 and int(packet[0][1]) == 1:
            return "current_dc"
        elif int(packet[12][1]) == 1 and int(packet[0][0]) == 1:
            return "voltage_ac"
        elif int(packet[12][1]) == 1 and int(packet[0][1]) == 1:
            return "voltage_dc"
        elif int(packet[11][1]) == 1 and int(packet[10][3]) == 0:
            return "resistance"
        elif int(packet[9][3]) == 1 and int(packet[12][1]) == 1:
            return "diode"
        elif int(packet[11][1]) == 1 and int(packet[10][3]) == 1:
            return "continuity"
        elif int(packet[11][0]) == 1:
            return "capacitance"
        elif int(packet[12][2]) == 1 or int(packet[10][1]) == 1:
            return "frequency"
        elif int(packet[13][1]) == 1:
            return "temperature"
        raise MultimeterFortuneFS9721Exception("Unsupported digital multimeter mode from packet")

    def _parse_packet_display_value(self, packet):
        if int(packet[1][0]) == 1:
            sign = -1
        else:
            sign = 1

        if int(packet[7][0]) == 1:
            multiplier = 0.1
        elif int(packet[5][0]) == 1:
            multiplier = 0.01
        elif int(packet[3][0]) == 1:
            multiplier = 0.001
        else:
            multiplier = 1

        def parse_digit(nibble_1, nibble_2):
            bits = "{}{}".format(nibble_1, nibble_2)[1:]
            if bits == "0000101":
                return "1"
            elif bits == "1011011":
                return "2"
            elif bits == "0011111":
                return "3"
            elif bits == "0100111":
                return "4"
            elif bits == "0111110":
                return "5"
            elif bits == "1111110":
                return "6"
            elif bits == "0010101":
                return "7"
            elif bits == "1111111":
                return "8"
            elif bits == "0111111":
                return "9"
            elif bits == "1111101":
                return "0"
            elif bits == "1101000":
                return "L"
            elif bits == "0000000":
                return ""
            else:
                raise MultimeterFortuneFS9721Exception("Unknown digit")

        digit_1 = parse_digit(packet[1], packet[2])
        digit_2 = parse_digit(packet[3], packet[4])
        digit_3 = parse_digit(packet[5], packet[6])
        digit_4 = parse_digit(packet[7], packet[8])

        try:
            number = int("{}{}{}{}".format(digit_1, digit_2, digit_3, digit_4))
        except ValueError:
            return None
        return sign * number * multiplier

    def _parse_packet_scale(self, packet):
        if int(packet[10][2]) == 1:
            scale = 1e6
            scale_name = "mega"
            scale_symbol = "M"
        elif int(packet[9][2]) == 1:
            scale = 1e3
            scale_name = "kilo"
            scale_symbol = "k"
        elif int(packet[10][0]) == 1:
            scale = 1e-3
            scale_name = "milli"
            scale_symbol = "m"
        elif int(packet[9][0]) == 1:
            scale = 1e-6
            scale_name = "micro"
            scale_symbol = "\u03BC"
        elif int(packet[9][1]) == 1:
            scale = 1e-9
            scale_name = "nano"
            scale_symbol = "n"
        else:
            scale = 1
            scale_name = None
            scale_symbol = None
        return scale, scale_name, scale_symbol

    def _parse_packet_units(self, packet):
        if int(packet[12][0]) == 1:
            unit_name = "amps"
            unit_symbol = "A"
        elif int(packet[12][1]) == 1:
            unit_name = "volts"
            unit_symbol = "V"
        elif int(packet[11][1]) == 1:
            unit_name = "ohms"
            unit_symbol = "\u03A9"
        elif int(packet[11][0]) == 1:
            unit_name = "farads"
            unit_symbol = "F"
        elif int(packet[12][2]) == 1:
            unit_name = "hertz"
            unit_symbol = "Hz"
        elif int(packet[10][1]) == 1:
            unit_name = "duty-cycle"
            unit_symbol = "%"
        elif int(packet[13][1]) == 1:
            unit_name = "celsius"
            unit_symbol = "C"
        else:
            raise MultimeterFortuneFS9721Exception("Unknown measurement units")
        return unit_name, unit_symbol

    def _parse_packet_low_battery(self, packet):
        if int(packet[12][3]) == 1:
            return True
        return False

    def _parse_packet_hold(self, packet):
        if int(packet[11][3]) == 1:
            return True
        return False

    def _parse_packet_relative(self, packet):
        if int(packet[11][2]) == 1:
            return True
        return False
