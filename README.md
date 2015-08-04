# python-nrpecheck

Provides the NrpeCheck base class for defining NRPE checks in python.


## Example Usage

```python
import sys
from nrpecheck import NrpeCheck

class HelloCheck(NrpeCheck):
    '''
    A simple example.
    '''
    def check(self):
        self.status = self.OK   # or self.WARNING or self.CRITICAL
        # message and perfdata can be single or multi-line.
        self.message = "Hello World"
        self.perfdata = sys.version
        
if __name__ == '__main__':
    HelloCheck().run()
```