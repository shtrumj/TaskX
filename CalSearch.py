from datetime import datetime, timedelta, timezone
from exchangelib import Account, Message, Configuration,Credentials, CalendarItem,DELEGATE, EWSDateTime, EWSTimeZone
import pytz

tz = EWSTimeZone.localzone()
creds = Credentials(
    username="trot\\task",
    password="__pool$&^2224"
)
config = Configuration(server='mail.trot.co.il', credentials=creds)

a = Account(
    primary_smtp_address="task@trot.co.il",
    autodiscover=False,
    config=config,
    access_type=DELEGATE
)

root = a.public_folders_root
pubs = (root.glob('*סידור עבודה'))



# Not all fields on an item support searching. Here's the list of options for
# Message items.
# print([f.name for f in Message.FIELDS if f.is_searchable])

# all_items = a.pubs.view()  # Get everything
# all_items_without_caching = a.inbox.all()
# Chain multiple modifiers to refine the query
# filtered_items = a.inbox.filter(subject__contains='foo')\
#   .exclude(categories__icontains='bar')
# Delete all items returned by the QuerySet
# status_report = a.inbox.all().delete()
# start = datetime.datetime(2022, 7, 17, tzinfo=a.default_timezone.localize(EWSDateTime.now()))
# end = datetime.datetime(2022, 7, 18, tzinfo=a.default_timezone)
# Filter by a date range
dt_start_time = datetime.strptime('2022-07-17 05:00:00', '%Y-%m-%d %H:%M:%S')
dt_end_time = datetime.strptime( '2022-07-17 17:00:00', '%Y-%m-%d %H:%M:%S')
# start = EWSDateTime.from_datetime(dt_start_time).astimezone(tz)
# end = EWSDateTime.from_datetime(dt_end_time).astimezone(tz)
start = EWSDateTime.from_datetime(dt_start_time).astimezone(tz)
end = EWSDateTime.from_datetime(dt_end_time).astimezone(tz)
items = pubs.view(start=start, end=end)
for item in items:
    print("%s\t%s" %(item.subject, item.start))