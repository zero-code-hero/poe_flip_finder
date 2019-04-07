
from poe_currency_flipper.types.currency import Currency


def currency_to_poe_trade_alt_codes(currency: Currency) -> int:
    if currency is Currency.CHAOS:
        return 4
    elif currency is Currency.REGRET:
        return 13
    elif currency is Currency.CHISEL:
        return 10
    elif currency is Currency.ALCHEMY:
        return 3
    elif currency is Currency.GCP:
        return 5
    elif currency is Currency.VAAL:
        return 16
    elif currency is Currency.SCOURING:
        return 11
    elif currency is Currency.DIVINE:
        return 15
    elif currency is Currency.FUSING:
        return 2
    elif currency is Currency.REGAL:
        return 14
    elif currency is Currency.CHAYULA:
        return 56
    elif currency is Currency.WHITE_SEXTANT:
        return 45
    elif currency is Currency.YELLOW_SEXTANT:
        return 46
    elif currency is Currency.RED_SEXTANT:
        return 47
    #elif currency is Currency.HORIZONS:
    #    return 515
    else:
        raise NotImplementedError
