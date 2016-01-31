#!/usr/bin/env python

import os
import time
import yaml

from slugify import slugify

DATA_FILE_PATH_PARTS = ['_data', 'members']
MEMBER_PATH_PARTS    = ['team', 'members']
TIMESTAMP_TIME = time.time()

def touch(filename, times=None):
    dirname = os.path.dirname(filename)
    try:
        # Attempt to create the parent directory.
        os.makedirs(dirname)
    except OSError:
        # The directory exists.
        pass
    finally:
        # Now create the file.
        with open(filename, 'a'):
            os.utime(filename, times)

def get_roster(roster):
    filename = '{roster}.yml'.format(roster=roster)
    filepath = os.path.abspath(os.path.join(*(DATA_FILE_PATH_PARTS+[filename])))
    with open(filepath) as f:
        roster = yaml.load(f)
    return roster

def name_for_member(member):
    name = '{first}{mi} {last}'.format(
        first   = member['first_name'],
        mi      = ' {}'.format(member['middle_initial']) if 'middle_initial' in member else '',
        last    = member['last_name']
    )
    return name

def filename_for_member(member):
    name = name_for_member(member)
    filename = '{name}.html'.format(name=slugify(name))
    return filename

def filepath_for_member(member):
    return os.path.abspath(os.path.join(*(MEMBER_PATH_PARTS+[filename_for_member(member)])))

def template_for_member(member, roster, index):
    name        = name_for_member(member)
    filename    = filename_for_member(member)
    template    = '\n'.join([
        "---",
        "layout: profile",
        "title: {name}",
        "permalink: /team/members/{filename}",
        "---",
        "",
        "{{% assign member_info = site.data.members.{roster}[{index}] %}}",
        "",
        "{{% include personal.html member=member_info %}}",
        "",
        "",
    ]).format(
        name        = name,
        filename    = filename,
        roster      = roster,
        index       = index,
    )
    return template

def process_roster(roster, members):
    # Iterate over the members and check that everyone has a page.
    for i in xrange(len(members)):
        member = members[i]
        filename = filepath_for_member(member)
        if not os.path.isfile(filename):
            # Create the file.
            touch(filename)
        try:
            # Attempt to create the parent directory.
            os.makedirs(os.path.dirname(filename))
        except OSError:
            # The directory exists.
            pass
        finally:
            # Fill the file with the template info. We overwrite this every time
            # because if the data file updates, then we need to update the array
            # indexing.
            text = template_for_member(member, roster, i)
            with open(filename, 'w') as f:
                f.write(text)
                os.utime(filename, (TIMESTAMP_TIME, TIMESTAMP_TIME))

if __name__ == '__main__':
    # Build the rosters.
    women = get_roster('women')
    men   = get_roster('men')
    # Process the rosters.
    process_roster('women', women)
    process_roster('men', men)
