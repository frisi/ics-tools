#!/usr/bin/env python

# small script to compare ical files

# used to compare ical files that got out of sync
# see  https://bugs.kde.org/show_bug.cgi?id=335090

# usage: compare_ics.py  ical-local-broken-sync.ics  ical-server.ics


from icalendar import Calendar
import sys
import difflib
from pprint import pprint

def get_key_value(a):
    val = ""
    if a.has_key("UID"):
        val = a["UID"]
    elif a.has_key("DTSTART"):
        val = a["DTSTART"]
    elif a.has_key("DESCRIPTION"):
        val = a["DESCRIPTION"]
    elif a.has_key("SUMMARY"):
        val = a["SUMMARY"]
    elif a.has_key("SUMMARY"):
        val = a["SUMMARY"]

    return val

def uid_sort(a, b):
    # fixme: we could protect us here against (invalid) UID-less components
    a_val = get_key_value(a)
    b_val = get_key_value(b)

    if a_val > b_val:
        return 1
    elif a_val < b_val:
        return -1
    else:
        return 0

if len(sys.argv) < 3:
    print "Usage: sort_ics.py in.ics out.ics"
    sys.exit(1)

# XXX prperly open/close files

cal1 = Calendar.from_ical(open(sys.argv[1], 'rb').read())
cal2 = Calendar.from_ical(open(sys.argv[2], 'rb').read())

def cal2dict(cal):
    cal_dict = {}
    for comp in cal.subcomponents:
        if not 'uid' in comp:
            #print "\n\n skip component \n" + comp.to_ical()
            continue
        uid = comp['uid']
        if uid in cal_dict:
            print "\n\n duplicate uid \n" + comp.to_ical()
            continue

        cal_dict[uid] = comp
    return cal_dict


def list_components(calendar_dict, keys):
    for key in keys:
        #print "\n\n" + calendar_dict[key].to_ical()
        print "\n * " + calendar_dict[key]['summary']

def list_differences(dict1, dict2):
    set1=set(dict1)
    set2=set(dict2)
    intersection = set1.intersection(set2)
    differ = difflib.Differ()
    print "nr items in both: %d" % len(intersection)
    for key in intersection:
        comp1 = dict1[key]
        comp2 = dict2[key]
        diff = list(differ.compare(comp1.to_ical().splitlines(1),
                                   comp2.to_ical().splitlines(1)))

        if diff:
            print "difference: " + key
            print "\n\n"
            pprint(diff)
        else:
            print "no difference: " + key


        #[s for s in difflib.ndiff(comp1.to_ical().split('\n'), comp2.to_ical().split('\n'))]



print "parsing calendars"

dict1 = cal2dict(cal1)
dict2 = cal2dict(cal2)

print "end parsing calendars"

set1 = set(dict1)
set2 = set(dict2)
intersect = set1.intersection(set2)


print "\n\n new in second file"
list_components(dict2, set2 - intersect)


print "\n\n only in first file"
list_components(dict1, set1 - intersect)



print "\n\n modified in second file"
list_differences(dict1, dict2)

