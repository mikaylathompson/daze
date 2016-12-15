# Daze

Daze is a day-based time-tracking command line utility.

My use for it (and therefore a lot of the terminology) is to track which days I'm working, in which state, or why I'm not.

My goal was to minimize the chance I would miss a day, have stats available for the year and month, and make easy to adjust errors.


### To address those goals:

1. Daily entry is done by means of cron job that checks every 15 minutes from 9am-8pm whether I've logged a location yet.  If not, it uses dialog boxes to ask me where I'm working and logs it.  There's a second cron job that creates a backup of the log file every few days.  This is primarily because I wanted to have a safety system while developing that would save me from a bug that deleted entries, for instance. But it seems like a mildly useful enough feature that I haven't deleted it.

2. Statistics can be checked in a "summary" or "calendar" view.

Summary lists number of days in each location, the earliest and latest dates in the logs, and whether any dates are missing.

![Successful summary](examples/summary.png)

![Summary with missing days](examples/summary_missing.png)

It also has a visual calendar mode.

![Calendar](examples/calendar.png)

3. Errors are easy to find with the calendar/summary mode and can be fixed through the interface by just doing a `daze add weekend 2016-04-09`, for instance.  Additionally, the storage format is a json that makes for very easy manual editing.


### Usage example:

```shell
$ daze add 2016-06-15 guilford
$ daze summary



### Improvements
- [ ] Implement a good frontend interface!
- [ ] Turns out there's a calendar module! Should definitely be used for my cal function.
- [ ] Build the setup function (create a ~/.daze directory with a log, backups, and settings, possibly cron job)
- [ ] Add a cli backup function
- [ ] Refactor out the apple dialogs
- [ ] Write up install instructions
- [ ] Implement the remove date function


# Musings on new Frontend interface:

`daze.py` should just be the API.  It should have `add`, `cal`, `summary`, etc. functions that return
nicely formatted data, without actually printing it (basically a somewhat more wrapped up version of
dazeutils, that doesn't have to know much about the underlying data. (in some ways, dazeutils is the
potentially-interchangable backend, the frontends are interchangable, and `daze.py` is the non-interchangable
glue between them.

Likely, the frontend will need a copy of the daze interface (object?) and daze interface needs the frontend.
(i.e. this is a two way link, not just daze calling frontend functions.)

-   In the daze-->frontend direction: display data (cal/summary), request information (location for add)
-   In the frontend-->daze direction: initiate actions (add, get summary, get cal data)

Perhaps have a 4th piece: a runner. Selects a frontend and connects it to daze







