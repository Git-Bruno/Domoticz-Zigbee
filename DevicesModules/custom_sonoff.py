#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Implementation of Zigbee for Domoticz plugin.
#
# This file is part of Zigbee for Domoticz plugin. https://github.com/zigbeefordomoticz/Domoticz-Zigbee
# (C) 2015-2024
#
# Initial authors: zaraki673 & pipiche38
#
# SPDX-License-Identifier:    GPL-3.0 license

from Modules.basicOutputs import write_attribute
from Modules.tools import get_device_config_param
from Modules.zigateConsts import ZIGATE_EP

SONOFF_MAUFACTURER_NAME = "SONOFF"
SONOFF_MANUFACTURER_ID = "1286"
SONOFF_CLUSTER_ID = "fc11"
SONOFF_ILLUMINATION_ATTRIBUTE = "2001"
SONOFF_MAX_TEMP = "0003"
SONOFF_MIN_TEMP = "0004"
SONOFF_MAX_HUMI = "0005"
SONOFF_MIN_HUMI = "0006"


def is_sonoff_device(self, nwkid):
    return self.ListOfDevices[nwkid]["Manufacturer"] == SONOFF_MANUFACTURER_ID or self.ListOfDevices[nwkid]["Manufacturer Name"] == SONOFF_MAUFACTURER_NAME


def sonoff_child_lock(self, nwkid, lock_mode):
    self.log.logging("Sonoff", "Debug", "sonoff_child_lock - Nwkid: %s Mode: %s" % (nwkid, lock_mode))
    write_attribute(self, nwkid, ZIGATE_EP, "01", SONOFF_CLUSTER_ID, SONOFF_MANUFACTURER_ID, "01", "0000", "10", "%02x" %lock_mode, ackIsDisabled=False)


def sonoff_open_window_detection(self, nwkid, detection):
    self.log.logging("Sonoff", "Debug", "sonoff_child_lock - Nwkid: %s Mode: %s" %(nwkid, detection))
    write_attribute(self, nwkid, ZIGATE_EP, "01", SONOFF_CLUSTER_ID, SONOFF_MANUFACTURER_ID, "01", "6000", "10", "%02x" %detection, ackIsDisabled=False)


def sonoff_temp_humi_ranges(self, nwkid, value):
    self.log.logging("Sonoff", "Debug", "sonoff_temp_humi_ranges - Nwkid: %s Mode: %s" %(nwkid, value))
    temp_max = get_device_config_param(self, nwkid, "SONOFF_TEMP_MAX")
    temp_min = get_device_config_param(self, nwkid, "SONOFF_TEMP_MIN")
    humi_max = get_device_config_param(self, nwkid, "SONOFF_HUMI_MAX")
    humi_min = get_device_config_param(self, nwkid, "SONOFF_HUMI_MIN")

    write_attribute(self, nwkid, ZIGATE_EP, "01", SONOFF_CLUSTER_ID, SONOFF_MANUFACTURER_ID, "01", SONOFF_MAX_TEMP, "29", "%04x" %temp_max, ackIsDisabled=False)
    write_attribute(self, nwkid, ZIGATE_EP, "01", SONOFF_CLUSTER_ID, SONOFF_MANUFACTURER_ID, "01", SONOFF_MIN_TEMP, "29", "%04x" %temp_min, ackIsDisabled=False)
    write_attribute(self, nwkid, ZIGATE_EP, "01", SONOFF_CLUSTER_ID, SONOFF_MANUFACTURER_ID, "01", SONOFF_MAX_HUMI, "21", "%04x" %humi_max, ackIsDisabled=False)
    write_attribute(self, nwkid, ZIGATE_EP, "01", SONOFF_CLUSTER_ID, SONOFF_MANUFACTURER_ID, "01", SONOFF_MIN_HUMI, "21", "%04x" %humi_min, ackIsDisabled=False)



SONOFF_DEVICE_PARAMETERS = {
    "SonOffTRVChildLock": sonoff_child_lock,
    "SonOffTRVWindowDectection": sonoff_open_window_detection,
    "SONOFF_TEMP_MAX": sonoff_temp_humi_ranges,
    "SONOFF_TEMP_MIN": sonoff_temp_humi_ranges,
    "SONOFF_HUMI_MAX": sonoff_temp_humi_ranges,
    "SONOFF_HUMI_MIN": sonoff_temp_humi_ranges
}
