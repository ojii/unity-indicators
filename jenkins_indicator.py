# -*- coding: utf-8 -*-
from collections import namedtuple
import appindicator
import gobject
import gtk
import json
import urllib2

JENKINS_URL = 'http://ci.django-cms.org'

class STATUS(object): pass
class NOT_OK(STATUS): pass
class OK(STATUS): pass
class FAIL(NOT_OK): pass
class UNSTABLE(NOT_OK): pass
class ABORTED(NOT_OK): pass
class GREY(NOT_OK): pass
class DISABLED(NOT_OK): pass
class IN_PROGRESS(STATUS): pass 
class UNKOWN(NOT_OK): pass

COLORS = {
    'red': FAIL,
    'yellow': UNSTABLE,
    'blue': OK,
    'disabled': DISABLED,
    'aborted': ABORTED,
    'grey': GREY,
}

for key, value in COLORS.items():
    COLORS['%s_anime' % key] = type('%s_IN_PROGRES' % value.__name__, (value, IN_PROGRESS,), {})


def _convert(color):
    return COLORS.get(color, UNKOWN)

Job = namedtuple('Job', ['name', 'status', 'url'])

def check():
    url = '%s/api/json' % JENKINS_URL
    handler = urllib2.urlopen(url)
    data = handler.read()
    obj = json.loads(data)
    jobs = []
    for job in obj['jobs']:
        jobs.append(Job(job['name'], _convert(job['color']), job['url']))
    overall_status = all([issubclass(job.status, OK) for job in jobs])
    return overall_status, jobs

if __name__ == "__main__":
    ind = appindicator.Indicator("example-simple-client",
                                 "indicator-messages",
                                 appindicator.CATEGORY_APPLICATION_STATUS)
    ind.set_status (appindicator.STATUS_ACTIVE)
    overall_status, jobs = check()
    ind.set_label("OK" if overall_status else "FAIL")

    # create a menu
    menu = gtk.Menu()

    # create some 
    menu_items = gtk.MenuItem("World!")

    menu.append(menu_items)

    menu_items.show()

    ind.set_menu(menu)
    
    gtk.main()
