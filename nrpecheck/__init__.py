"""
nrpecheck

Provides the NrpeCheck base class for defining NRPE checks in python.
------------------------------------
import sys
from nrpecheck import NrpeCheck

class HelloCheck(NrpeCheck):
    '''
    A simple example.
    '''
    def check(self):
        self.status = self.OK   # or self.WARNING or self.CRITICAL
        # output and perfdata can be single or multi-line.
        self.output = "Hello World"
        self.perfdata = sys.version
        
if __name__ == '__main__':
    HelloCheck().run()
"""
# Copyright 2015 Dave Gabrielson <dave.gabrielson@gmail.com>.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys

class NrpeCheck(object):
    """
    Base class for running NRPE checks.
    Reference: https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/3/en/pluginapi.html
    """
    OK = 0
    WARNING = 1
    CRITICAL = 2
    UNKNOWN = 3
    
    MAX_MESSAGE_LENGTH = 4096

    
    def __init__(self, *args, **kwargs):
        self.status = None
        self.output = None
        self.perfdata = None
 
 
    def format_message(self):
        """
        Construct the appropriate output message based on strings
        ``self.output`` and ``self.perfdata``.
        """
        if self.output is None:
            self.output = ''
        if self.perfdata is None:
            self.perfdata = ''
            
        output_lines = self.output.split('\n')
        perfdata_lines = self.perfdata.split('\n')
        
        message = output_lines[0]
        if perfdata_lines[0]:
            message += u'|' + perfdata_lines[0]
        if output_lines[1:] or perfdata_lines[1:]:
            message += u'\n'
        if output_lines[1:]:
            message += u'\n'.join(output_lines[1:])
        if perfdata_lines[1:]:
            message += u'|' + u'\n'.join(perfdata_lines[1:])
        return message
        
    
    def check(self):
        """
        Do the check.
        Set ``self.status`` to one of ``NrpeCheck.OK``, ``NrpeCheck.WARNING``,
        or ``NrpeCheck.CRITICAL``.
        Set ``self.output`` and ``self.perfdata`` as relevant single or 
        multi-line strings as needed.
        """
        raise RuntimeError("Subclasses must define the check() method.")

        
    def run(self):
        """
        Run the check and return appropriately.
        """
        self.check()
        if self.status not in [NrpeCheck.OK, NrpeCheck.WARNING, NrpeCheck.CRITICAL]:
            self.status = NrpeCheck.UNKNOWN
        sys.stdout.write(self.format_message()[:self.MAX_MESSAGE_LENGTH])
        sys.exit(self.status)
