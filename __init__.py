# Copyright 2016 Mycroft AI, Inc.
#
# This file is part of Mycroft Core.
#
# Mycroft Core is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Mycroft Core is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Mycroft Core.  If not, see <http://www.gnu.org/licenses/>.
from os.path import dirname

from adapt.intent import IntentBuilder

from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger


import requests

__author__ = 'Rahul Kumar Shandilya'

LOGGER = getLogger(__name__)


class ItsmUserSkill(MycroftSkill):
    def __init__(self):
        super(ItsmUserSkill, self).__init__(name="ItsmUserSkill")

    def initialize(self):
        self.load_data_files(dirname(__file__))
        
        
        itsm_user_intent = IntentBuilder("itsmuserintent"). \
            require("ItsmUserKeyword").build()
        self.register_intent(itsm_user_intent, self.handle_itsm_user_intent)
        
    def handle_itsm_user_intent(self, message):
        url = 'https://dev22921.service-now.com/api/now/table/incident?sysparm_query=assigned_to%3D66e1f49edb5d13006b72712ebf9619c2%5Epriority%3D1&sysparm_display_value=true&sysparm_exclude_reference_link=true&sysparm_fields=caller_id%2Cshort_description%2Cstate'
        user = '531834'
        pwd = 'Welcome!2345'
        headers = {"Content-Type":"application/json","Accept":"application/json"}
        # Do the HTTP request
        response = requests.get(url, auth=(user, pwd), headers=headers )
        # Check for HTTP codes other than 200
        if response.status_code != 200: 
            print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
            exit()
        # Decode the JSON response into a dictionary and use the data
        data = response.json()
        length = len(data['result'])
        x = 0
        r = data['result']
        #number = r['result']['number']
        detail = ""
        for x in range(0, length):
            detail += "Your incident {} is {} having caller as {} with ShortDescription {} and currently work is {} ".format(x+1,  r[x]['number'], r[x]['caller_id'],r[x]['short_description'], r[x]['state'])
            x += 1
        self.speak("You have {} incidents with Priorty 1".format(length))
        self.speak(detail)
        

    def stop(self):
        pass


def create_skill():
    return ItsmUserSkill()
