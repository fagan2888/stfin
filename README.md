# finlib
A simple library for collecting financial data from the web.

The functions implemented so far:
1. ``get_yahoo_quote``: Fetches price data for a symbol by querying finance.yahoo.
2. ``get_sp_500``: Fetches the list of companies included in the S&P500 index.

``demo.py`` demonstrates basic usage. Run it from the command line using ``python demo.py``. The output should look something like:

```
➜ ~/git/finlib (master) python demo.py 
TESTING GET_SP500()
The first few symbols:
     MMM: 3M Company
     ABT: Abbott Laboratories
    ABBV: AbbVie Inc.
    ABMD: ABIOMED Inc
     ACN: Accenture plc
    ATVI: Activision Blizzard
    ADBE: Adobe Systems Inc
     AMD: Advanced Micro Devices Inc
     AAP: Advance Auto Parts
     AES: AES Corp

TESTING GET_YAHOO_QUOTE()
Query: https://query1.finance.yahoo.com/v8/finance/chart/FB?symbol=FB&interval=1d&period1=1501443768&period2=1532893368
Symbol: FB
Currency: USD
The first time point: 20170731
The last  time point: 20180727
The first few closing prices:
20170731: 169.25
20170801: 169.86000061
20170802: 169.300003052
20170803: 168.589996338
20170804: 169.619995117
20170807: 171.979995728
20170808: 171.229995728
20170809: 171.179992676
20170810: 167.399993896
20170811: 168.080001831
... (241 more)

Done.

```

