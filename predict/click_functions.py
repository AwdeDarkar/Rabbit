"""
click functions
====================================================================================================

Command-line interface that uses click to directly (local to the server) interface with the
prediction system.

----------------------------------------------------------------------------------------------------

**Created**
    11.08.18
**Updated**
    11.08.18 by Darkar
**Author**
    Darkar
**Copyright**
    This code is Free and Open Source for any purpose; it is provided as-is without warranty.
"""

import click
from flask.cli import with_appcontext

from .api_functions import create_predictions, select_list
from ..database import manage_db

@click.command("construct")
@click.option("-n", "--name")
@click.option("-d", "--description")
@click.option("-e", "--event", nargs=2, type=click.Tuple([str, float]), multiple=True)
@with_appcontext
def construct_command(name, description, event):
    """ Create a new prediction """
    prediction = {}

    if name:
        prediction["name"] = name
    else:
        prediction["name"] = click.prompt("Name of the prediction ", type=str)

    if description:
        prediction["description"] = description
    else:
        prediction["description"] = click.prompt("Description of the prediction ", type=str)

    if not event:
        s = click.prompt("List of events followed by float probability (space separated) ")
        lst = s.split(" ")
        event = []
        for itm in lst:
            if event and not isinstance(event[-1], tuple):
                event[-1] = (event[-1], itm)
            else:
                event.append(itm)
    prediction["events"] = {}
    for evt in event:
        prediction["events"][evt[0]] = evt[1]

    db = manage_db.get_db()
    create_predictions(db, [prediction])

@click.command("list-all")
@with_appcontext
def list_all_command():
    """ List all of the predictions in the database """
    db = manage_db.get_db()
    preds = select_list(db)
    for pred in preds:
        click.echo(pred)
