from poe_currency_flipper.factories.currency_to_poe_trade_alt_codes import currency_to_poe_trade_alt_codes
from poe_currency_flipper.types.currency import Currency
from structlog import get_logger
from requests import get
from bs4 import BeautifulSoup
from typing import List, Tuple
import re

logger = get_logger(__name__)


def get_rates(from_c: Currency, to_c: Currency) -> List[Tuple[float, float]]:

    url = f"http://currency.poe.trade/search?league=Synthesis&online=x&stock=&want={currency_to_poe_trade_alt_codes(to_c)}&have={currency_to_poe_trade_alt_codes((from_c))}"
    response = get(url=url)
    if response.status_code != 200:
        raise Exception("Bad response code.")

    # Make sane
    soup = BeautifulSoup(response.text, 'html.parser')

    rates: List[Tuple[float, float]] = []
    skip = False
    # Get listed offers
    for listing in soup.findAll("div", {"class": "large-3 columns displayoffer-centered"}):

        if skip:
            # LOL, good luck figuring out why i did this.
            skip = not skip
            continue
        # Group 1 is the base, group 2 is the target
        search = re.search(r"1\D+(\d*\.?\d*)", listing.text)
        if not search:
            logger.debug("Could not parse exchange rate for entry", text=listing.text)
        rates.append(
            # First value is always 1.
            # 1 of x is worth z of y.
            (1, float(search.group(1)))
        )
        skip = not skip

    return rates

