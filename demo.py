import finlib.core as finlib

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



