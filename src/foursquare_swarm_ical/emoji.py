import sys

from foursquare import Foursquare  # type: ignore [import]
import yaml

if sys.version_info >= (3, 9):
    import importlib.resources as importlib_resources  # isort: skip
else:
    import importlib_resources  # isort: skip


def make_venues_yaml(access_token: str) -> None:
    client = Foursquare(access_token=access_token)
    tree = client.venues.categories()

    tree = strip(tree)

    with open("venues.yaml", "w", encoding='utf-8') as f:
        yaml.safe_dump(tree, stream=f, sort_keys=False, allow_unicode=True)


def strip(category_raw):
    category = {}
    if 'name' in category_raw and category_raw['name']:
        category['name'] = category_raw['name']
    if 'id' in category_raw and category_raw['id']:
        category['id'] = category_raw['id']
    if 'categories' in category_raw and category_raw['categories']:
        category['categories'] = [strip(subcategory) for subcategory in category_raw['categories']]
    return category


def fill_defaults(category, default=None):
    if 'emoji' not in category or not category['emoji']:
        category['emoji'] = default
    if 'categories' in category and category['categories']:
        for subcategory in category['categories']:
            fill_defaults(subcategory, category['emoji'])


def index_by_id(index, category):
    if 'id' in category and category['id']:
        index[category['id']] = category
    if 'categories' in category and category['categories']:
        for subcategory in category['categories']:
            index_by_id(index, subcategory)


class Emojis:
    def __init__(self):
        with importlib_resources.files(__package__).joinpath("emoji.yaml").open('r', encoding='utf-8') as f:
            self.tree = yaml.safe_load(f)

        fill_defaults(self.tree)

        self.index = {}
        index_by_id(self.index, self.tree)

    def get_emoji_for_venue(self, venue, default='📍'):
        category = [c for c in venue['categories'] if 'primary' in c and c['primary']]
        category = category[0] if category else None
        if not category:
            return default

        category = self.index.get(category['id'])
        if not category or 'emoji' not in category or not category['emoji']:
            return default
        else:
            return category['emoji']
