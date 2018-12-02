#!c:\Python34\python.exe
# -*- coding: utf-8 -*-

# Copyright (C) 2018, CERN
# This software is distributed under the terms of the GNU General Public
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".
# In applying this license, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as Intergovernmental Organization
# or submit itself to any jurisdiction.

import re
import logging

from base.Utils import Utils
from base.RestLogger import RestLogger
from suds.client import Client
from suds.transport.http import HttpAuthenticated
from suds import WebFault



class Vidyo:

    TIMEOUTDEFAULT = 30
    AUTOMUTE_API_PROFILE = "NoAudioAndVideo"

    def __init__(self, username, password, URL_WSDL):
        self.credentials = dict([('username', username), ('password', password)])
        self.auth = HttpAuthenticated(**self.credentials, timeout=Vidyo.TIMEOUTDEFAULT)
        self.URL_WSDL = URL_WSDL
        self.client = Client(url=self.URL_WSDL, location=re.sub(r'\?wsdl$', '', self.URL_WSDL),
                        transport=self.auth)
        # enable extra logging from suds module
        logging.getLogger('suds.client').setLevel(logging.DEBUG)

    def _Find_Room(self, extension):
        filter_ = self.client.factory.create('Filter')
        filter_.query = extension
        filter_.limit = 40
        filter_.dir = 'DESC'

        counter = 0

        while True:
            filter_.start = counter * filter_.limit
            response = self.client.service.getRooms(filter_)
            if not response.total:
                return None
            for room in response.room:
                if int(room.extension) == int(extension):
                    RestLogger.debug('Room: {} has been found.'.format(room))
                    return room
                else:
                    RestLogger.debug('Dismissing room extension {}'.format(room.extension))
                counter += 1

    def UpdateRoomOwner(self, extension, owner):
        RestLogger.debug("Looking for room with extension: {} to change owner to {}".format(extension, owner))
        room = self._Find_Room(extension)
        if room:
            RestLogger.debug("Room with extension: {} found, Room_id is {}".format(extension, room.roomID))
            room.ownerName = owner
            try:
                self.client.service.updateRoom(room.roomID, room)
            except WebFault as e:
                RestLogger.debug("Got exception {}".format(e))

    def PrintWSDLdefinition(self):
        print(self.client)

    def CreatePublicRoom(self, name, owner, islocked=False, hasPIN=False, hasmoderatorPIN=False):
        RestLogger.debug('Trying to create room: {} belonging to {}'.format(name, owner))
        try:
            room = self.client.factory.create('Room')
            room.name = name
            room.ownerName = owner
            room.RoomType ='Public'
            room.extension = Utils.GenerateNumber(10999, 5)
            room.groupName = 'default'
            room.description = "Test room, it can be deleted"
            room.RoomMode = self.client.factory.create('RoomMode')
            if islocked:
                room.RoomMode.isLocked ='true'
            else:
                room.RoomMode.isLocked = 'false'
            if hasPIN:
                room.RoomMode.hasPIN = 'true'
                room.RoomMode.roomPIN = Utils.GenerateNumber('11', 4)
            else:
                room.RoomMode.hasPIN = 'false'
            if hasmoderatorPIN:
                room.RoomMode.hasModeratorPIN = 'true'
                room.RoomMode.moderatorPIN = Utils.GenerateNumber('11', 4)
            else:
                room.RoomMode.hasModeratorPIN = 'false'
            RestLogger.debug('Trying to create room: {}'.format(room))
            obj = self.client.service.addRoom(returnObjectInResponse='true', room=room)
            if obj.OK == "OK":
                RestLogger.debug('Room created with id {} and extension {}'.format(obj.room.roomID, obj.room.extension))
            else:
                RestLogger.debug('Room not created with id {}'.format(room))
        except WebFault as e:
            RestLogger.debug("Got exception {}".format(e))

    def ToggleRoomProfile(self, roomID, profile=None):
        RestLogger.debug('Trying to set room_id: {} to profile: {}'.format(roomID, profile))
        try:
            if profile:
                RestLogger.debug('Roomid {} setting profile to: {}'.format(roomID, profile))
                obj = self.client.service.setRoomProfile(roomID, profile)
            else:
                RestLogger.debug('Roomid {} setting profile to None'.format(roomID))
                obj = self.client.service.removeRoomProfile(roomID)
            #if obj.OK == "OK":
            #    RestLogger.debug('Room created with id {}'.format(obj.room.roomID))
            #else:
            RestLogger.debug('Roomid {} profile operation finished with result: {}'.format(roomID, obj))
        except WebFault as e:
            RestLogger.debug("Got exception {}".format(e))

    def GetRoomProfile(self, roomID):
        RestLogger.debug('Trying to get profile for roomID: {}'.format(roomID))
        try:
            answer = self.client.service.getRoomProfile(roomID)
            if bool(answer):
                if answer.roomProfileName == Vidyo.AUTOMUTE_API_PROFILE:
                    RestLogger.debug('Roomid {} has automute profile set'.format(roomID))
                    return True
            RestLogger.debug('Roomid {} has no automute profile set'.format(roomID))
            return False
        except WebFault as e:
            RestLogger.debug("Got exception {}".format(e))