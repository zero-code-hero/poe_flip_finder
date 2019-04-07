
from poe_currency_flipper.logic.poe_trade import get_rates
from poe_currency_flipper.types.currency import Currency
from fractions import Fraction
from poe_currency_flipper.utils.clear_screen import clear_screen
import time
from typing import List, Tuple, Dict
import numpy
from pandas import DataFrame, Series
import math


WATCHED_RATES = []

for x in list(Currency):
    if x is Currency.CHAOS:
        continue

    WATCHED_RATES.append(
        (Currency.CHAOS, x)
    )

def get_average(rates: List[float]) -> float:
    average = 0
    for x in rates:
        average += x
    average = average / len(rates)
    average = round(average, 3)
    average = math.ceil(average * 100) / 100
    return average


if __name__ == "a__main__":
    while True:
        def _create_matrix() -> DataFrame:
            # create our rows
            rows: Dict[str, List[float]] = {}
            for _c in list(Currency):
                values = []
                for x in list(Currency):
                    print(x, _c)
                    if x == _c:
                        values.append(1)
                    else:
                        values.append(get_average([x[1] for x in get_rates(_c, x)[2:15]]))
                rows[_c.value] = values

            return DataFrame.from_dict(
                rows,
                orient="index",
                columns=list(Currency)
            )
        df = _create_matrix()

        # Our starting currency, in this case one chaos.
        vector = [0] * len(Currency)
        vector[0] = 1
        vector = Series(vector, index=list(Currency))

        # Res is our starting currencys converted to others.
        res = df.dot(vector)

        sum = Series([0] * len(Currency), index=list(Currency))
        for i in range(len(Currency)):
            vec = [0] * len(Currency)
            vec[i] = res[i]
            vec = numpy.array(vec)
            series2 = numpy.array(vec)
            sum += df.T.dot(series2)
        print(sum)


        #print("===res===")
        #print(res)
        #print("===df.T.dot(res)===")
        #print(df.T.dot(res))
        #print("===df.T.dot===")
        #print(df.T)



if __name__ == "__main__":

    while True:
        msg = ""
        for exchange in WATCHED_RATES:
            #Get the rates, anything past 10 results can be considered to far down to fuck with.
            rates = [x[1] for x in get_rates(exchange[1], exchange[0])][:10]
            rates_inverse = [x[1] for x in get_rates(exchange[0], exchange[1])][:10]
            # Throw out duplicates
            #rates = list(set(rates))
            #rates_inverse = list(set(rates_inverse))

            # We're going to take the average of the top 15 traders
            # People don't like to give up chaos so we need to be competitive when buying chaos, and within the top ~5

            # Also throw out the first 2 people since most of the time its just people trying to sell fast.
            average = get_average(rates)
            # When flipping back we can take our time since people tend to be looser when converting to chaos.
            average_inverse = get_average(rates_inverse)

            # when buying x for y we want to round up for ours and down for theirs.

            # we want at least 10%, anything less if not worth the time.
            profit_on_100 = (100 * average) * average_inverse

            msg += f"{exchange[0].value} to {exchange[1].value} average {average} {Fraction(average).limit_denominator(max_denominator=30)}\n"
            msg += f"{exchange[1].value} to {exchange[0].value} average {average_inverse} {Fraction(average_inverse).limit_denominator(max_denominator=30)}\n"
            msg += f"Profit with 100 {profit_on_100 - 100} {exchange[0].value}\n"

            # If I have 100 chaos starting and make this flip, will I profit?
            # print(f"Profit with 100 chaos conversion")
            # msg += f"100 {exchange[0].value} -> {100 * average} {exchange[1].value} -> {(100 * average) * average_inverse} {exchange[0].value}\n"
            # msg += f"100 {exchange[1].value} -> {100 * average_inverse} {exchange[0].value} -> {(100 * average_inverse) * average} {exchange[1].value}\n"

            #break
        print("\n" * 80)
        print(msg)
        time.sleep(10)

"""
for exchange in WATCHED_RATES:
    current_value = 100
    converted_value = None
    print(exchange)

    for idx, _c in enumerate(exchange):
        if idx == len(exchange) - 1:
            break

        rates = get_rates(exchange[idx], exchange[idx + 1])
        average_rate = get_average([x[1] for x in rates[2:15]])

        converted_value = current_value * average_rate
        print(f"Step {idx}: {current_value} {exchange[idx].value} -> {converted_value} {exchange[idx+1].value} @ {average_rate}")

        current_value = converted_value
        #print(rates)
"""


