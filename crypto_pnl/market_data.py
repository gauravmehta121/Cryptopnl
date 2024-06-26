# MIT License
#
# Copyright (c) 
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from .core import *
from .asset import *
import os

# An example of market data
#
# - downloaded from Binance Market Data: https://www.binance.com/en/landing/data
# - data format is described here: https://github.com/binance/binance-public-data
#
# Headers look like this:
#  open_timestamp, open_price, high_price, low_price, close_price, volume, close_timestamp, ...
#
# NOTE: There is no header row in market data files.
#
# Data looks like this:
#  1622851200000,390.68000000,408.87000000,387.60000000,408.00000000,194592.68850000,1622854799999,77913286.76816900,128810,104749.99380000,41959412.36701900,0
#  1622854800000,408.00000000,414.76000000,404.76000000,411.66000000,149213.25410000,1622858399999,61119124.08516800,85638,80303.78440000,32883076.55872100,0
#  1622858400000,411.63000000,413.74000000,407.81000000,411.96000000,93883.26250000,1622861999999,38547160.91696800,41956,46960.26150000,19281907.03656700,0
#


class MarketData:
    def __init__(self, path, main,
            unix, open_price, high_price, low_price, close_price, *_unused
        ):
        self.symbol_traded = os.path.split(path)[1].split(main,1)[0]
        self.symbol_main = main
        self.unix = unix
        self.date = get_datetime_from_timestamp(int(unix))
        self.open_price = parse_price(open_price)
        self.high_price = parse_price(high_price)
        self.low_price = parse_price(low_price)
        self.close_price = parse_price(close_price)
    
    @property
    def value(self):
        return (self.open_price + self.close_price + self.high_price + self.low_price) / 4

def load_market_data(path):
    market_data_csv = load_csv(path)
    for row in market_data_csv:
        try:
            yield MarketData(path, FIAT_EXCHANGE_SYMBOL, *row)
        except Exception as err:
            print(err, row)
            raise
