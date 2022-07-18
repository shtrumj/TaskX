from datetime import datetime, timedelta
from exchangelib import DELEGATE, Account, Credentials, Configuration, CalendarItem, ExtendedProperty, Folder, \
    FolderCollection, EWSDateTime, EWSTimeZone
from datetime import datetime, timedelta, tzinfo
import dateutil.tz

import pytz
try:
    import zoneinfo
except ImportError:
    from backports import zoneinfo
from exchangelib import EWSTimeZone, EWSDateTime, EWSDate, UTC, UTC_NOW

start_date = []
subject = []
events_today = {}
tz = EWSTimeZone('Asia/Jerusalem')
tz = EWSTimeZone.localzone()
dateutil_tz = dateutil.tz.gettz('Europe/Copenhagen')
tz = EWSTimeZone.from_timezone(dateutil_tz)


year = datetime.now().year
month = datetime.now().month
day = datetime.now().day

tomorrowY = (datetime.now() + timedelta(days=1)).year
tomorrowM = (datetime.now() + timedelta(days=1)).month
tomorrowD = (datetime.now() + timedelta(days=1)).day

yesterdayY = (datetime.now() + timedelta(days=-1)).year
yesterdayM = (datetime.now() + timedelta(days=-1)).month
yesterdayD = (datetime.now() + timedelta(days=-1)).day

yesterdayEWS = EWSDateTime(int(yesterdayY), int(yesterdayM), int(yesterdayD), tzinfo=tz)
tomorrowEWS = EWSDateTime(int(tomorrowY), int(tomorrowM), int(tomorrowD), tzinfo=tz)
todayEWS = EWSDateTime(int(year), int(month), int(day), tzinfo=tz)
creds = Credentials(
    username="trot\\jonathan",
    password="Gib$0n579!"
)
config = Configuration(server='mail.trot.co.il', credentials=creds)

account = Account(
    primary_smtp_address="jonathan@trot.co.il",
    autodiscover=False,
    config=config,
    access_type=DELEGATE
)

root = account.public_folders_root
pubs = (root.glob('*סידור עבודה'))
error = 'unknown timezone ID'

try:
    for occurrence in pubs.view(start=yesterdayEWS, end=tomorrowEWS):
        print(type(yesterdayEWS))
        # subject.append(occurrence.subject)
        # start_date.append(occurrence.start)
except:
    pass

print(subject[2], start_date[2])
