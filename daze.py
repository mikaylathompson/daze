import click
import dazeutils as d
from datetime import date, timedelta
import subprocess
import sys


@click.group()
def cli():
    pass


@cli.command()
@click.option('--log', type=click.Path(exists=True))
@click.option('--month', '-m', type=click.INT)
def summary(log, month):
    daze = loadLog(log)
    if (month is not None):
        year = date.today().year
        first = date(year, month, 1)
        last = date(year, month + 1, 1) - timedelta(days=1)
        s = daze.summarize(firstdate=first, lastdate=last)
    else:
        s = daze.summarize()
    # summarize values: placeDict, number of days, first date, last date
    for (p, v) in s[0].items():
        click.echo("%s: %d" % (p, v))

    missing_days = ((s[3] - s[2]) - timedelta(days=s[1]-1)).days

    click.echo("\nBetween %s and %s:" % (s[2].isoformat(), s[3].isoformat()))
    click.secho("%d total dates" % s[1], bg='green', nl=(missing_days == 0))
    if missing_days > 0:
        click.secho("with %d missing days." % missing_days, bg='red')


@cli.command()
@click.argument('place', required=False)
@click.argument('strdate', required=False)
@click.option('--log', type=click.Path(exists=True))
def add(place, strdate, log):
    daze = loadLog(log)
    if place is None:
        place = getPlaceFromDialog()
    if strdate is None:
        strdate = date.today().isoformat()
    daze.add(strdate, place)
    if log is None:
        d.dazeToFile(daze)
    else:
        d.dazeToFile(daze, log)

@cli.command()
@click.option('--cron')
@click.option('--log', type=click.Path(exists=True))
def checkToday(cron, log):
    daze = loadLog(log)
    if cron is not None:
        if date.today() in daze.dateDict.keys():
            sys.exit(1)
        else:
            sys.exit(0)
    click.echo(date.today() in daze.dateDict.keys())
    return date.today() in daze.dateDict.keys()


@cli.command()
@click.option('--log', type=click.Path(exists=True))
def calendar(log):
    daze = loadLog(log)
    log = daze.dateDict
    s, ndates, firstdate, lastdate = daze.summarize()
    places = sorted(s, key=s.get, reverse=True)
    colors = ['green', 'magenta', 'white', 'cyan', 'blue', 'red', 'yellow']
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    dates = [firstdate + timedelta(days=i) for i in range((lastdate - firstdate).days + 1)]

    matches = {p:c for (p, c) in zip(places, colors)}

    for (p, c) in matches.items():
        click.secho(p, bg=c, bold=True)

    for date in dates:
        if (date.day == 1 or date == firstdate):
            click.echo('')
            click.echo("\n" + months[date.month - 1])
            if (date.isoweekday() != 7):
                click.echo(" " * 3 * date.isoweekday(), nl=False)
        if date in log:
            p = log[date]
            click.secho("%s" % str(date.day).rjust(3), bg=matches[p], nl=(date.isoweekday() == 6))
        else:
            click.secho("%s" % str(date.day).rjust(3), nl=(date.isoweekday() == 6))

    click.echo('\n\n\n')



def loadLog(log):
    if log is not None:
        return d.fileToDaze(log)
    return d.fileToDaze()


def getPlaceFromDialog():
    workOrNot = '''
        tell app "System Events" to display dialog "Working today?" with title "Daze" buttons {"Yes", "No"} default button "Yes"
    '''
    workingWhere = '''
        tell app "System Events" to display dialog "Where?" with title "Daze" buttons {"Guilford", "New York", "Other"} default answer "" default button "Other"
    '''
    notWorkingWhy = '''
        tell app "System Events" to display dialog "Why not?" with title "Daze" buttons {"Weekend", "Holiday", "Other"} default answer "" default button "Weekend"
    '''
    def dialogResponseToDict(rawResponse):
        clipped = str(rawResponse)[2:-3]
        split = [c.strip().split(':') for c in clipped.split(',')]
        return {c[0]:c[1] for c in split}

    answer_workOrNot = dialogResponseToDict(subprocess.check_output(['osascript', '-e', workOrNot]))
    if answer_workOrNot["button returned"] == "Yes":
        subanswer = dialogResponseToDict(subprocess.check_output(['osascript', '-e', workingWhere]))
    else:
        subanswer = dialogResponseToDict(subprocess.check_output(['osascript', '-e', notWorkingWhy]))
    if subanswer['text returned'] == "":
        return subanswer['button returned'].lower()
    return subanswer['text returned'].lower()
