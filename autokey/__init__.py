# -*- coding: utf-8 -*-

"""AutoKey integration for albert launcher.

This extension adds the autokey launch functions to the albert launcher, launch \
your favorite AutoKey scripts using ak run <script name> quickly open the AK \
with ak open <script name> to change the script.

Synopsis: ak [run|open] <script/phrase>"""

from albertv0 import *
import os
from time import sleep

from subprocess import check_output, Popen


__iid__ = "PythonInterface/v0.1"
__prettyname__ = "AutoKey Integration"
__version__ = "1.0"
__trigger__ = "ak "
__author__ = "Sam Sebastian"
__dependencies__ = ["autokey"]

iconPath = iconLookup("autokey")

autokey_items = []


# Can be omitted
def initialize():
    fetch_script_list()
    pass

def fetch_script_list():
    out = check_output(["/home/sam/autokey/autokey-run", "-ls", "blank"])
    lines = out.decode("utf-8").strip().split("\n")
    for line in lines:
        autokey_items.append(line.split(" ",1))

# Can be omitted
def finalize():
    pass


def handleQuery(query):
    if not query.isTriggered:
        return

    # Note that when storing a reference to query, e.g. in a closure, you must not use
    # query.isValid. Apart from the query beeing invalid anyway it will crash the appplication.
    # The Python type holds a pointer to the C++ type used for isValid(). The C++ type will be
    # deleted when the query is finished. Therfore getting isValid will result in a SEGFAULT.

    # if query.string.startswith("run"):
    #     return Item(id=__prettyname__,
    #                 icon=os.path.dirname(__file__)+"/autokey.svg",
    #                 text="Run a script",
    #                 subtext="Run script: "+query.string)
        

    # if query.string.startswith("open"):
    #     raise ValueError('EXPLICITLY REQUESTED TEST EXCEPTION!')

    info(query.string)
    info(query.rawString)
    info(query.trigger)
    info(str(query.isTriggered))
    info(str(query.isValid))

    critical(query.string)
    warning(query.string)
    debug(query.string)
    debug(query.string)

    results = []

    if query.string.startswith("run"):
        print("test")

        for item in autokey_items:
            item_type = item[0]
            item_name = item[1]
            if query.string[4:].lower() in item_name.lower():
                ret_item = build_item(item_type,item_name)
                results.append(ret_item)


    # Api v 0.2
    info(configLocation())
    info(cacheLocation())
    info(dataLocation())

    return results

def build_item(item_type, item_name):
    if item_type=='Script':
        flag = '-s'
    elif item_type=='Folder':
        flag = '-f'
    elif item_type=='Phrase':
        flag = '-p'
    item = Item()
    item.icon = iconPath
    item.text = 'AutoKey %s' % item_name
    item.subtext = 'Run AutoKey %s' % item_type
    item.completion = __trigger__ + item_name
    def run_script():
        Popen(['autokey-run', flag, item_name])
    item.addAction(FuncAction("Run "+item_type, run_script))
    return item

