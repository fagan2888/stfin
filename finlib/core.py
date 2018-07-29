import datetime
import urllib2
import json
from bs4 import BeautifulSoup as bs
from collections import namedtuple
import re

from helpers import totimestamp

def get_yahoo_quote(symbol, interval = "1m", time_string = "1week", start_datetime = None, end_datetime = None):
    """ Queries finance.yahoo.com for price data on the specified symbol. 
    Returns the results as a (success, data) tuple.
    
    INPUTS:

    symbol: 
    The string symbol, e.g. 'MSFT'

    interval: 
    The sample interval, e.g. '1d' for daily prices. Should be one of:
    ['1m', '1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']

    time_string: 
    Specifies the date range of interest relative to today. 
    E.g. '2days' fetches data for the last two days.
    The format should be an integer followed by one of 
    'minutes', 'hours','days', or 'weeks'. The trailing 's' is not important.
    
    start|end_datetime: 
    Datetime objects to specify the date range directly.
    
    RETURNS:
    A (success, data) tuple. 'success' is boolean. 'data' is always a dictionary 
    containing at least the fields "query" containing the urllib query string, and 
    "error" containing any error messages. If the query succeeded, the following 
    fields will also be present: 

    t: (datetime) Time for each price.
    open,close,high,low: (float) The price data.
    volume: (int) The volume data.
    granularity: (string) The granularity of the data.
    currency: (string) The currency of the price
    symb: (string) The symbol.

    EXAMPLES:

    success, data = get_yahoo_quote("MSFT", interval = "1m", time_string = "1day")
    success, data = get_yahoo_quote("FB", interval = "1d", time_string = "52weeks")

    """        
    query = "https://query1.finance.yahoo.com/v8/finance/chart/{}?symbol={}".format(symbol, symbol)

    valid_intervals = [u'1m', u'1d', u'5d', u'1mo', u'3mo', u'6mo', u'1y', u'2y', u'5y', u'10y', u'ytd', u'max']
    if interval not in valid_intervals:
        raise ValueError("interval must be in {}".format(valid_intevals))
    
    query += "&interval=" + interval

    ## Determine the desired time interval
    now = datetime.datetime.now()
    if time_string: # Should be [0-9]+[mins|hours|days|weeks] e.g. '1day' or '2weeks'
        time_string = time_string.lower()
        if "min" in time_string:
            kwargs = {"minutes": -int(time_string.split("min")[0])} 
        elif "hour" in time_string:
            kwargs = {"hours":   -int(time_string.split("hour")[0])} 
        elif "day" in time_string:
            kwargs = {"days":    -int(time_string.split("day")[0])}
        elif "week" in time_string:
            kwargs = {"weeks":   -int(time_string.split("week")[0])}
        else:
            raise ValueError("time_string must be [0-9]+[mins|hours|days|weeks].")            

        end_datetime   = now
        start_datetime = end_datetime + datetime.timedelta(**kwargs)
    else:
        end_datetime   = end_datetime   if end_datetime   else now
        start_datetime = start_datetime if start_datetime else end_datetime - datetime.timedelta(days=-1)
        
    query += "&period1={}&period2={}".format(totimestamp(start_datetime), totimestamp(end_datetime))

    try:
        data = json.loads(urllib2.urlopen(query).read())
    except Exception as e:
        return False, {"error":"Read error: " + str(e), "query":query}
        
    # Unpack the data
    error  = "Query error: {}".format(data["chart"]["error"])
    payload = data["chart"]["result"][0] 
    times = [datetime.datetime.fromtimestamp(t) for t in payload["timestamp"]]
    quote = payload["indicators"]["quote"][0]
    curr  = payload["meta"]["currency"]
    gran  = payload["meta"]["dataGranularity"]
    symb  = payload["meta"]["symbol"]

    return True, {"t":times, 
                  "open":quote["open"],
                  "close":quote["close"], 
                  "high":quote["high"],
                  "low":quote["low"], 
                  "volume":quote["volume"], 
                  "currency":curr,
                  "granularity":gran,
                  "symbol":symb,
                  "error":error,
                  "query":query}    

    
def get_sp500():
    """ Scrapes Wikipedia for the list of S&P500 companies.
    The result is returned as a list of namedtuples.
    Each named tuple has the same fields as the columns in 
    the Wikipedia table which aren't just hyperlinks.

    Example: Get all the ticker symbols.
    
    records = get_sp500()
    symbs = [r.tickersymbol for r in records]
    """

    query = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    html = urllib2.urlopen(query).read()
    soup = bs(html, "html.parser")

    # Get the first table
    table = soup.find("table")
    # Get all the rows
    rows = table.find_all("tr")
    header_row = rows[0]
    data_rows  = rows[1:]

    # The first row is a header containing the fields
    all_fields = [re.sub("[^a-z]", "", t.text.lower()) for t in header_row.find_all('th')]
    fields_to_drop = ["secfilings"] # This is just a hyperlink to the reports
    fields_to_keep = [f for f in all_fields if f not in fields_to_drop]

    Record = namedtuple("Record", " ".join(fields_to_keep))
    records = []
    for t in data_rows: # Skip the first row, it's the hader
        td = t.find_all('td')
        kwargs = dict(zip(fields_to_keep, [td[all_fields.index(f)].text.strip() for f in fields_to_keep]))
        records.append(Record(**kwargs))
    
    return records
