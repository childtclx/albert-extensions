"""search files of markdown module.
Synopsis: <triger> <search-files>
"""

import os
import sys
import re
import json

from albertv0 import *


__iid__ = "PythonInterface/v0.1"
__prettyname__ = "Search files Markdowns"
__trigger__ = "smd "
__version__ = "0.1"
# __author__ = "Joseph Lin"
__author__ = "childtclx"  # modify from Joseph Lin
__dependencies__ = []

ICON_PATH = iconLookup('typora')


CONFIGURATION_DIR = os.path.join(
    os.getenv('HOME'), ".config", 'albert',
    'org.albert.extension.python')

if not os.path.exists(CONFIGURATION_DIR):
    os.path.mkdir(CONFIGURATION_DIR)
elif not os.path.isdir(CONFIGURATION_DIR):
    raise RuntimeError(f"{CONFIGURATION_DIR} should be a directory")

CONF_FILE = os.path.join(CONFIGURATION_DIR, 'search_markdown.json')

try:
    '''
    /<path>/<to>/<CONF_FILE>
    {"markdown_files_directory": "/<path>/", "trigger_len": 3}
    '''
    with open(CONF_FILE, 'r') as fp:
        conf_d = json.loads(fp.read())
        MARKDOWN_FILES_DIRECTORY = conf_d['markdown_files_directory']
        TRIGGER_LEN = conf_d['trigger_len']
except Exception as err:
    raise RuntimeError('{}'.format(err))


def handleQuery(query):
    if not query.isValid or not query.isTriggered:
        return

    if len(query.string) < TRIGGER_LEN:
        return

    search_str = query.string

    err_msg = Item(id="", icon=ICON_PATH, actions=[],
                   completion="", urgency=ItemBase.Notification,
                   text="", subtext="")
    ret_items = [err_msg, ]

    try:
        # pp = os.popen(
        #     f"cd {MARKDOWN_FILES_DIRECTORY} && grep \"{search_str}\" ./ -rRni --include=\"*.md\"", 'r')
        pp = os.popen(
            f"cd {MARKDOWN_FILES_DIRECTORY} && find . -iname \"*{search_str}*.md\" | grep -v '/\.'", 'r')
        list_ = []
        for line in pp:
            # ret = re.match(r'^(\./)([\w-]+.md):([\d]+):(.*)', line)
            ret = re.match(r'^(\.\/)(.*)/(.*.md)$', line)
            item = Item(id='', icon=ICON_PATH,
                        actions=[
                            ProcAction('Open Markdown File by Typora',
                                       ['/usr/bin/typora', os.path.join(MARKDOWN_FILES_DIRECTORY, ret.group(2) + '/' + ret.group(3))]),
                        ],
                        text='', subtext='',
                        completion='', urgency=ItemBase.Notification)
            # item.text = ret.group(4)
            item.text = ret.group(3)
            item.subtext = ret.group(2)
            list_.append(item)
        ret_items = list_
    except Exception as err:
        warning("{!r}".format(err))
        ret_items[0].text = str(err)
        ret_items[0].subtext = "Internal Error!"

    return ret_items
