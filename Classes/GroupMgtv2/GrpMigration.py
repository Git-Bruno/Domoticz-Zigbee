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


from Modules.domoticzAbstractLayer import (domoticz_error_api,
                                           domoticz_log_api,
                                           domoticz_status_api)


def migrateIfTradfriRemote(self, GrpId):

    if "Tradfri Remote" not in self.ListOfGroups[GrpId]:
        return
    NwkId = self.ListOfGroups[GrpId]["Tradfri Remote"]["Device Addr"]
    domoticz_status_api("Migration of Ikea Tradfri %s in Group %s" % (NwkId, GrpId))

    if "Ep" not in self.ListOfGroups[GrpId]["Tradfri Remote"]:
        self.ListOfGroups[GrpId]["Tradfri Remote"]["Ep"] = "01"

    if "IEEE" not in self.ListOfGroups[GrpId]["Tradfri Remote"]:
        if NwkId in self.ListOfDevices:
            self.ListOfGroups[GrpId]["Tradfri Remote"]["IEEE"] = self.ListOfDevices[NwkId]["IEEE"]
        else:
            self.logging("Error", "Cannot migrate Tradfri Remote . don't find Nwkid %s" % NwkId)
            del self.ListOfGroups[GrpId]["Tradfri Remote"]


def migrateTupleToList(self, GrpId, tupleItem):

    lenItem = len(tupleItem)
    if lenItem not in [2, 3]:
        self.logging("Error", "For Group: %s unexpected Group Device %s droping" % (GrpId, str(tupleItem)))
        return

    if lenItem == 2:
        NwkId, Ep = tupleItem
        if "IEEE" not in self.ListOfDevices[NwkId]:
            self.logging("Error", "For Group: %s unexpected Group Device %s droping" % (GrpId, str(tupleItem)))
            return
        Ieee = self.ListOfDevices[NwkId]["IEEE"]
        # Migrate from Tuple to List
        self.ListOfGroups[GrpId]["Devices"].remove((NwkId, Ep))
        self.ListOfGroups[GrpId]["Devices"].append([NwkId, Ep, Ieee])

    elif lenItem == 3:
        # Migrate from Tuple to List
        NwkId, Ep, Ieee = tupleItem
        self.ListOfGroups[GrpId]["Devices"].remove((NwkId, Ep, Ieee))
        self.ListOfGroups[GrpId]["Devices"].append([NwkId, Ep, Ieee])

    domoticz_status_api("--- --- NwkId: %s Ep: %s Ieee: %s" % (NwkId, Ep, Ieee))
    if NwkId not in self.ListOfDevices:
        self.logging("Error", "migrateTupleToList - NwkId: %s not found in current database" % NwkId)
        if Ieee not in self.IEEE2NWK:
            return
        NwkId = self.IEEE2NWK[Ieee]
        domoticz_status_api("---> Retreive new NwkId: %s from Ieee: %s" % (NwkId, Ieee))

    if "GroupMemberShip" not in self.ListOfDevices[NwkId]:
        self.ListOfDevices[NwkId]["GroupMemberShip"] = {}

    if Ep not in self.ListOfDevices[NwkId]["GroupMemberShip"]:
        self.ListOfDevices[NwkId]["GroupMemberShip"][Ep] = {}

    if GrpId not in self.ListOfDevices[NwkId]["GroupMemberShip"][Ep]:
        self.ListOfDevices[NwkId]["GroupMemberShip"][Ep][GrpId] = {}

    self.ListOfDevices[NwkId]["GroupMemberShip"][Ep][GrpId]["Status"] = "OK"
    self.ListOfDevices[NwkId]["GroupMemberShip"][Ep][GrpId]["TimeStamp"] = 0


def GrpMgtv2Migration(self):

    domoticz_status_api("Group Migration to new format")
    for GrpId in self.ListOfGroups:
        domoticz_status_api("--- GroupId: %s" % GrpId)
        migrateIfTradfriRemote(self, GrpId)

        for item in list(self.ListOfGroups[GrpId]["Devices"]):
            migrateTupleToList(self, GrpId, item)
