#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Multimeter class for the Voltcraft VC870

    This multimeter uses its own protocol which is described here:
    - https://asset.conrad.com/media10/add/160267/c1/-/en/000124603IN01/information-124603-voltcraft-vc870-hand-multimeter-digital-cat-iii-1000-v-cat-iv-600-v-anzeige-counts-40000.pdf
    - https://sigrok.org/wiki/Voltcraft_VC-870
    
    This class is written to be used with the new USB HID cable "UNI-T UT-D04".
    The USB HID-UART bridge is either Hoitek HE2325U or WCH CH9325.
    If someone wants to implement this for serial connection override the methods
    interface_open, interface_close, interface_readbytes, interface_flush.
    Or place these methods in classes: Serial and USB HID.
    
    In order to run this use the model name  "Voltcraft_VC870" and the connect paramter "usb:1a86.e008"
    (assuming this is the correct VID.PID). "usb:" might be omitted and "1a86:e008" is also accepted.
    
    Using the USB HID on Linux:
    1. Ensure the permissions allow you to read the device, make a udev rule otherwise.
    2. Sometimes the CH9325 cannot be accessed unless reset with the following script:
        #!/bin/bash
        for dat in /sys/bus/usb/devices/*; do
          if test -e $dat/manufacturer; then
            grep "WCH.CN" $dat/manufacturer > /dev/null && echo auto > ${dat}/power/level && echo 0 > ${dat}/power/autosuspend
          fi
        done
       But this might be fixed by the USB reset after initialization.
    
    Thanks to the following projects (which knowledge is partially used here):
    - sigrok (https://github.com/martinling/libsigrok/blob/master/src/dmm/vc870.c)
    - https://github.com/jsyk/VC870_USB_Datalog
    - http://erste.de/UT61/index.html
    - https://github.com/pklaus/ut61e_python
"""

import logging
import math
import platform
import re
import time

import usb.core
import usb.util

from ..exceptions import MultimeterException
from ..multimeters.MultimeterBase import MultimeterBase

UART_SPEED = 9600

PACKET_RETRY_LIMIT = 3
PACKET_SIZE = 23
PACKET_TERMINATOR = "\r\n"
ALLOWED_DATA = range(0x30, 0x40)

logger = logging.getLogger(__name__)


class MultimeterVC870USBHIDException(MultimeterException):
    pass


class MultimeterVC870USBHID(MultimeterBase):
    dev = None
    ep = None
    buffer = ""

    def __init__(self, connect):
        super().__init__()
        self.interface_open(connect)

    def __del__(self):
        self.interface_close()

    def interface_open(self, connect):
        connect_info = re.match(r"(?:usb:)?([a-fA-F0-9]{4})[:.]([a-fA-F0-9]{4})", connect)
        if len(connect_info.groups()) != 2:
            raise MultimeterVC870USBHIDException("Could not read VID/PID from connect string: {}".format(connect))

        self.dev = usb.core.find(idVendor=int(connect_info.group(1), 16), idProduct=int(connect_info.group(2), 16))

        if self.dev is None:
            raise MultimeterVC870USBHIDException("Could not find USB device")
        else:
            logger.debug(
                "Connected to VID={}, PID={} successfully".format(connect_info.group(1), connect_info.group(2))
            )

        # This reset helps to readout the CH9325
        self.dev.reset()
        if platform.system() != "Windows":
            if self.dev.is_kernel_driver_active(0) is True:
                logging.debug("Detaching kernel driver before using")
                self.dev.detach_kernel_driver(0)
            else:
                logging.debug("Kernel driver already detached")

        # Set default configuration and get it
        self.dev.set_configuration()
        cfg = self.dev.get_active_configuration()

        # get an endpoint instance
        interface_number = cfg[(0, 0)].bInterfaceNumber
        alternate_setting = usb.control.get_interface(self.dev, interface_number)
        intf = usb.util.find_descriptor(cfg, bInterfaceNumber=interface_number, bAlternateSetting=alternate_setting)
        # match the first input endpoint (we are doing uART RX here only)
        self.ep = usb.util.find_descriptor(
            intf, custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_IN
        )

        if self.ep is None:
            raise MultimeterVC870USBHIDException("No endpoint found on device")

        uart_conf = list(UART_SPEED.to_bytes(4, byteorder="little"))
        uart_conf.append(0x03)
        # dev.ctrl_transfer(bmRequestType, bmRequest, wValue, wIndex, payload)
        assert self.dev.ctrl_transfer(
            usb.util.CTRL_TYPE_CLASS | usb.util.CTRL_RECIPIENT_INTERFACE | usb.util.CTRL_OUT,
            9,  # HID set_report
            0x0300,  # HID feature, report number 0
            0,  # interface 0
            uart_conf,
        )

    def interface_close(self):
        if self.dev:
            logger.debug("Closing USB connection")
            self.dev.reset()
            usb.util.dispose_resources(self.dev)

    def interface_flush(self):
        self.buffer = ""

    def interface_read(self, size=1, timeout_ms=3000):
        # Always read from the endpoint even if data in the buffer is available. This ensures no packet is missed
        time_limit = time.time() + timeout_ms / 1000
        while True:
            answer = self.dev.read(self.ep.bEndpointAddress, self.ep.wMaxPacketSize, timeout=timeout_ms)
            if (len(answer) > 1) and (answer[0] & 0xF0 == 0xF0):
                # get payload size
                nbytes = answer[0] & 0x7
                if nbytes > 0:
                    if len(answer) < nbytes + 1:
                        raise MultimeterVC870USBHIDException("More bytes announced then sent")
                    payload = answer[1 : nbytes + 1]
                    # The highest bit must be removed from each payload byte (might be 1 or 0)
                    # In this protocol all data is represented in printable ascii chars in the range 0x30 - 0x3F
                    data = [chr(b & (~(1 << 7))) for b in payload]
                    data = "".join(data)
                    self.buffer += data

            if len(self.buffer) >= size:
                break
            if time.time() > time_limit:
                raise MultimeterVC870USBHIDException("No bytes received. Multimeter connected and set to PC mode?")

        ret_val = self.buffer[:size]
        self.buffer = self.buffer[size:]
        return ret_val

    def get_reading(self):
        return self.parse_packet(self.receive_packet())

    def receive_packet(self):
        packet = ""
        retries = 0
        bytes_to_read = PACKET_SIZE
        packet_data_size = PACKET_SIZE - len(PACKET_TERMINATOR)

        self.interface_flush()
        while bytes_to_read > 0:
            received_data = self.interface_read(bytes_to_read)
            logging.debug("Interface read {} bytes: {}".format(bytes_to_read, repr(received_data)))
            packet += received_data
            terminator_pos = packet.find(PACKET_TERMINATOR)

            # Best case: we got the complete packet
            if terminator_pos == packet_data_size:
                packet = packet[:packet_data_size]
                illegal_bytes = [x for x in packet if ord(x) not in ALLOWED_DATA]
                if len(illegal_bytes) == 0:
                    bytes_to_read = 0
                else:
                    # Corrupt packet: Illegal chars in data string - start over
                    packet = ""
                    bytes_to_read = PACKET_SIZE
                    self.interface_flush()
            elif terminator_pos < 0:
                # Corrupt packet: No terminator found at all - start over
                packet = ""
                bytes_to_read = PACKET_SIZE
                self.interface_flush()
            else:
                packet = packet[terminator_pos + len(PACKET_TERMINATOR) :]
                illegal_bytes = [x for x in packet if ord(x) not in ALLOWED_DATA]
                if len(illegal_bytes) == 0:
                    # We got a partial packet. Try to read the rest
                    bytes_to_read = PACKET_SIZE - len(packet)
                else:
                    # Corrupt packet: Illegal bytes found in partial string - start over
                    packet = ""
                    bytes_to_read = PACKET_SIZE
                    self.interface_flush()

            retries += 1
            if (retries > PACKET_RETRY_LIMIT) and (bytes_to_read > 0):
                raise MultimeterVC870USBHIDException(
                    "Too many invalid responses after {} retries".format(PACKET_RETRY_LIMIT)
                )

        return packet

    def parse_packet(self, packet):
        mode = self._parse_packet_operation_mode(packet)
        value, aux_value = self._parse_packet_display_value(packet)
        value *= mode[2]
        flags = self._parse_packet_flags(packet)

        if "overflow" in flags or "open" in flags:
            value = math.inf
            aux_value = math.inf

        timestamp_this = time.time_ns()
        time_interval = int(timestamp_this - self.timestamp_previous)
        self.timestamp_previous = timestamp_this

        return_dict = {
            "reading": {
                "operation_mode": mode[0],
                "value": value,
                "unit": mode[1],
                "aux_value": None,
                "aux_unit": None,
            },
            "instrument": {
                "module": __name__.split(".")[-1],
                "active_flags": flags,
            },
            "time": {
                "elapsed": (timestamp_this - self.timestamp_start) * 1e-9,
                "interval": time_interval * 1e-9,
                "timestamp": timestamp_this * 1e-9,
                "unit_name": "second",
                "unit_symbol": "s",
            },
        }

        # In certain modes AUX values are available
        if len(mode) == 5:
            aux_value *= mode[4]
            return_dict["reading"]["aux_value"] = aux_value
            return_dict["reading"]["aux_unit"] = mode[3]

        return return_dict

    def _parse_packet_operation_mode(self, packet):
        operation_id = packet[:2]

        # The first two bytes define the measurement mode (function code + function select code)
        # Resulting from these two bytes the following parameters can be derived:
        # 1. Operation mode
        # 2. Physical unit that is measured
        # 3. Base factor to calculate the SI value from the display value
        # In some operation modes there is an auxiliary value measured and displayed.
        # In this case the value tuple is extended by:
        # 4. Physical unit of the auxiliary measurement
        # 5. Base factor to calculate the SI value from the auxiliary value
        id_to_op_mode = {
            "00": ("DCV", "V", 1e-4),
            "01": ("ACV", "V", 1e-4),
            "10": ("DCmV", "V", 1e-5),
            "11": ("TEMP", "°C", 1e-1),
            "20": ("RES", "Ohm", 1e-2),
            "21": ("CTN", "Ohm", 1e-2),
            "30": ("CAP", "F", 1e-12),
            "40": ("DIO", "V", 1e-4),
            "50": ("FREQ", "Hz", 1),
            "51": ("(4~20)mA%%", "%%", 1),
            "60": ("DCuA", "A", 1e-8),
            "61": ("ACuA", "A", 1e-8),
            "70": ("DCmA", "A", 1e-6),
            "71": ("ACmA", "A", 1e-6),
            "80": ("DCA", "A", 1e-3),
            "81": ("ACA", "A", 1e-3),
            "90": ("Act+Apar_Power", "W", 0.1, "VA", 0.1),
            "91": ("PowFactor+Freq", "cos_fi", 1e-3, "Hz", 0.1),
            "92": ("VoltEff+CurrEff", "V", 0.1, "A", 0.1),
        }

        operation_mode = id_to_op_mode.get(operation_id)
        if operation_mode is None:
            raise MultimeterVC870USBHIDException("Unsupported digital multimeter mode from packet")

        return operation_mode

    def _parse_packet_display_value(self, packet):
        value = int(packet[3:8])
        aux_value = int(packet[8:13])

        sign = 1
        aux_sign = 1

        status = ord(packet[15]) & 0b1111
        if status & 0b100:
            sign = -1
        if status & 0b1000:
            aux_sign = -1

        multiplier = 10 ** int(packet[2])

        value *= sign * multiplier
        aux_value *= aux_sign * multiplier

        return value, aux_value

    def _parse_packet_flags(self, packet):
        # rs232_dat[13] Simulate strip tens digit --> discard
        # rs232_dat[14] Simulate strip the single digit --> discard
        status = ord(packet[15]) & 0b1111
        option1 = ord(packet[16]) & 0b1111
        option2 = ord(packet[17]) & 0b1111
        option3 = ord(packet[18]) & 0b1111
        option4 = ord(packet[19]) & 0b1111

        active_flags = []

        if status & 0b10:
            active_flags.append("battery")
        if status & 0b1 or option2 & 0b1000:
            active_flags.append("overflow")
        if option1 & 0b1000:
            active_flags.append("max")
        if option1 & 0b100:
            active_flags.append("min")
        if option1 & 0b10:
            active_flags.append("maxmin")
        if option1 & 0b1:
            active_flags.append("rel")
        if option2 & 0b100 or option4 & 0b1:
            active_flags.append("open")
        if option2 & 0b10:
            active_flags.append("manual")
        if option2 & 0b1:
            active_flags.append("hold")
        if option3 & 0b1000:
            active_flags.append("light")
        if option3 & 0b10:
            active_flags.append("warning")
        if option4 & 0b1000:
            active_flags.append("misplug_warn")
        if option4 & 0b100:
            active_flags.append("lo")
        if option4 & 0b10:
            active_flags.append("hi")

        # They are always on and therefore not very helpful
        # if option3 & 0b100:
        # active_flags.append("usb")
        # if option3 & 0b1:
        # active_flags.append("auto_power")

        return "|".join(active_flags)
