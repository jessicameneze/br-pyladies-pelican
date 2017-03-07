import os
from datetime import datetime

import yaml
from facebook import GraphAPI


PYLADIES_FACEBOOK_PAGES = [
    'pyladies',
    'PyLadiesBrazil',
    'PyLadiesSP',
    'pyladiescps',
    'PyLadiesTeresina',
    'PyLadiesNatal',
    'PyLadiesDuqueDeCaxias',
    'pyladiesvale',
    'pyladiesfloripa',
    'PyLadiesCuritiba',
    'pyladiesdf',
    'pyladiesrp',
    'PyLadiesSaoCarlos',
    'pyladiesbh',
    'pyladiespucrio',
    'PyLadiesFortaleza',
    'pyLadiesPHB',
    'fundao.pyladies',
    'pyladiesrio',
    'PyLadiesPicos',
    'pyladiesbelem',
    'PyLadiesSalvador',
    'pyladiesrecife',
    'PyLadiesMaceio',
    'pyladiespoa',
    'PyLadiesSLZ',
]


def load_facebook_events(nodes, token=os.environ.get('FACEBOOK_TOKEN')):
    """
    Load events from Facebook pages to the events file.

    ..important:

        In order for this function to work, you need to to provide a valid
        Facebook Graph API token. You can get yours easily on
        https://developers.facebook.com/tools/explorer

    :param nodes: Facebook nodes to load public events from.
    :param token: Facebook Graph API token.
    """

    # Facebook settings
    graph = GraphAPI(access_token=token)

    with open('data/events.yml', 'r') as events_file:
        existing_events = yaml.load(events_file)

    # Get facebook metadata on existing entries
    facebook_ids = {entry.get('facebook-id') for entry in existing_events}

    fetched_events = []

    for node in nodes:
        event_node = "{}/events".format(node)
        node_events = graph.get_object(event_node, limit=1000)

        for event in node_events['data']:

            # If event already exists, just ignore
            if event['id'] in facebook_ids:
                continue

            format_date = datetime.strptime(event['start_time'],
                                            '%Y-%m-%dT%H:%M:%S%z')

            fetched_events.append({
                'name': event['name'],
                'url': 'https://facebook.com/{}'.format(event['id']),
                'local': event.get('place', {}).get('name', ''),
                'date': format_date.strftime('%d-%m-%Y'),
                'facebook_id': str(event['id'])
            })

    with open('data/events.yml', 'a') as events_file:
        for entry in fetched_events:
            events_file.write('\n')
            yaml.dump([entry], events_file,
                      default_flow_style=False,
                      allow_unicode=True)
