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
        self.output = "Hello World"
        self.perfdata = sys.version
        
if __name__ == '__main__':
    HelloCheck().run()
```

## Configure Nagios

This is **not** meant to provide working knowledge of configuring Nagios,
just a quick reference for adding your own NRPE checks.

### Configure Client NRPE Server

Edit `/etc/nagios/nrpe.cfg` or an appropriate config in `/etc/nagios/nrpe.d/`
(Ubuntu).

```
command[check_hello]=/usr/local/sbin/hellocheck.py
```

Restart the `nagios-nrpe-server` service (Ubuntu).

### Configure Nagios Server

Edit an appropriate config in `/etc/nagios3/conf.d/` (Ubuntu).

```
define service {
    service_description		nrpecheck test
    check_command		    check_nrpe_1arg!check_hello
    use				        generic-service
    notification_interval	0
}
```

Restart the `nagios3` service (Ubuntu).