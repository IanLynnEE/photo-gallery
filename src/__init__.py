from pathlib import Path

from . import single_page
from . import all_page
from . import from_soup


for website in single_page.support_websites:
    Path(f'static/{website}').mkdir(parents=True, exist_ok=True)
    Path(f'static/{website}.txt').touch(exist_ok=True)
for website in all_page.support_websites:
    Path(f'static/{website}').mkdir(parents=True, exist_ok=True)
    Path(f'static/{website}.txt').touch(exist_ok=True)
for website in from_soup.support_websites:
    Path(f'static/{website}').mkdir(parents=True, exist_ok=True)
