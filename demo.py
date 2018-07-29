import finlib.core as finlib

print "Testing get_sp500()".upper()
records = finlib.get_sp500()
print "The first few symbols:"
print "\n".join(["{:>8}: {}".format(r.tickersymbol, r.security) for r in records][:10])
print ""

print "Testing get_yahoo_quote()".upper()
# Get the daily data for Facebook for the last year.
success, data  = finlib.get_yahoo_quote("FB", interval = "1d", time_string = "52weeks")
if success:
    print "Query: {}".format(data["query"])
    print "Symbol: {}".format(data["symbol"])
    print "Currency: {}".format(data["currency"])
    print "The first time point: {}".format(data["t"][0].strftime("%Y%m%d"))
    print "The last  time point: {}".format(data["t"][-1].strftime("%Y%m%d"))
    print "The first few closing prices:"
    for i in range(10):
        print "{}: {}".format(data["t"][i].strftime("%Y%m%d"), data["close"][i])
    print "... ({} more)".format(len(data["t"])-10)

else:
    print "FAILED\n{}".format(data["error"])
print ""

print "Done."



