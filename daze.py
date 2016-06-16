import click
import dazeutils as d
from datetime import date, timedelta
import subprocess
import sys

@click.group()
@click.option('--log', type=click.Path(exists=True), help="Select a log. Default is the one specified in $DAZE/settings.json.")
@click.pass_context
def cli(ctx, log):
    ctx.obj = dict()
    ctx.obj['log'] = log
    ctx.obj['daze'] = d.fileToDaze(log)
    pass


@cli.command()
@click.option('--month', '-m', type=click.INT, help="Show summary for a specific month (in the current year).")
@click.pass_context
def summary(ctx, month):
    """Show a summary of all logged days that includes days in each location, as well as if any days are missing."""
    daze = ctx.obj['daze']
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
@click.pass_context
def add(ctx, place, strdate):
    """Add (or overwrite) an entry to the log. Enter the place followed by the date as YYYY-MM-DD."""
    daze = ctx.obj['daze']
    if place is None:
        place = getPlaceFromDialog()
    if strdate is None:
        strdate = date.today().isoformat()
    daze.add(strdate, place)
    d.dazeToFile(daze, ctx.obj['log'])

@cli.command()
@click.option('--cron', help="If cron is on, there is no output but the exit value is non-zero if today has not been logged.")
@click.pass_context
def checkToday(ctx, cron):
    """Check whether today has been logged.  Returns true/false."""
    daze = ctx.obj['daze']
    if cron is not None:
        if date.today() in daze.dateDict.keys():
            sys.exit(1)
        else:
            sys.exit(0)
    click.echo(date.today() in daze.dateDict.keys())
    return date.today() in daze.dateDict.keys()


@cli.command()
@click.option('--month', '-m', type=click.INT, help="Show summary for a specific month (in the current year).")
@click.pass_context
def calendar(ctx, month):
    """Display a calendar of all logged dates."""
    daze = ctx.obj['daze']
    log = daze.dateDict
    if (month is not None):
        year = date.today().year
        first = date(year, month, 1)
        last = date(year, month + 1, 1) - timedelta(days=1)
        s, ndates, firstdate, lastdate = daze.summarize(firstdate=first, lastdate=last)
    else:
        s, ndates, firstdate, lastdate = daze.summarize()
    places = sorted(s, key=s.get, reverse=True)
    colors = ['green', 'magenta', 'white', 'cyan', 'blue', 'red', 'yellow']
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    dates = [firstdate + timedelta(days=i) for i in range((lastdate - firstdate).days + 1)]

    matches = {p:c for (p, c) in zip(places, colors)}

    for (p, c) in matches.items():
        click.secho(p, bg=c, bold=True)

    for _date in dates:
        if (_date.day == 1 or _date == firstdate):
            click.echo('')
            click.echo("\n" + months[_date.month - 1])
            if (_date.isoweekday() != 7):
                click.echo(" " * 3 * _date.isoweekday(), nl=False)
        if _date in log:
            p = log[_date]
            click.secho("%s" % str(_date.day).rjust(3), fg='black', bg=matches[p], nl=(_date.isoweekday() == 6))
        else:
            click.secho("%s" % str(_date.day).rjust(3), fg='black', nl=(_date.isoweekday() == 6))

    click.echo('\n\n\n')


@cli.command()
@click.option('strdate', required=True)
def remove(ctx, strdate):
    click.echo("Not yet implemented.")

@cli.command()
@click.pass_context
def setup(ctx):
    click.echo("Not yet implemented.")

@cli.command()
@click.pass_context
def backup(ctx):
    click.echo("Not yet implemented.")


def getPlaceFromDialog():
    workOrNot = '''
        tell app "System Events" to display dialog "Working today?" with title "Daze" buttons {"Yes", "No"} default button "Yes" giving up after 15
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

