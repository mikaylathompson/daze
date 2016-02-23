import click
import dazeutils as d
from datetime import date, timedelta


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
@click.argument('place')
@click.argument('strdate', required=False)
@click.option('--log', type=click.Path(exists=True))
def add(place, strdate, log):
    daze = loadLog(log)
    if strdate is None:
        strdate = date.today().isoformat()
    daze.add(strdate, place)
    if log is None:
        d.dazeToFile(daze)
    else:
        d.dazeToFile(daze, log)


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
