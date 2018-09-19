from __future__ import unicode_literals
from .http import HttpFD
try:
    import urllib.request as compat_urllib_request
except ImportError:  # Python 2
    import urllib2 as compat_urllib_request
import threading
class HttpHB(HttpFD):
    def real_download(self, filename, info_dict):
        result = False
        beating = 1
        if 'heartbeat_url'in info_dict:
            def heart_beat():
                if(beating):
                    try:
                        data = info_dict['heartbeat_data'].encode("utf-8")
                        compat_urllib_request.urlopen(url=info_dict['heartbeat_url'], data=data)
                        print('heart beat!')
                    except Exception as e:
                        print('heart beat fail: ' + str(e))
                        pass
                    if not result:
                        timer = threading.Timer(25, heart_beat)
                        timer.start()

            heart_beat()
        try:
            result = super(HttpHB, self).real_download(filename, info_dict)
        except:
            #just to make absolutely sure that we stop the beating so the thread dies
            beating = 0
            raise
        return result
        
