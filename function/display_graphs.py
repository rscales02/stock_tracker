import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mpl_dates
import numpy as np
import mpl_finance as mpf
from datetime import date


def display_graphs():
    # Switch between different visual graphs
    display = [True]

    while not display == []:
        choice = input('Which graph? "Returns", "Candle stick" or "Exit": ').lower()
        switcher = {
            'r': return_and_log_return,
            'c': candle_stick,
            'e': display.pop,
            'default': invalid_entry
        }
        switcher.get(choice, 'default')()


def invalid_entry():
    print('Invalid entry, please try again')


def return_and_log_return():
    pickle = pd.read_pickle('ticker.pkl')
    pickle = pickle['Close']
    log_returns = np.log(pickle).diff()

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 12))

    for c in log_returns:
        ax1.plot(log_returns.index, log_returns[c].cumsum(), label=str(c))
        ax2.plot(log_returns.index, 100 * (np.exp(log_returns[c].cumsum()) - 1), label=str(c))

    ax1.set_ylabel('Cumulative log returns')
    ax1.legend(loc='best')

    ax2.set_ylabel('Total relative returns (%)')
    ax2.legend(loc='best')

    plt.show()


def candle_stick():
    pickle = pd.read_pickle('ticker.pkl')
    for stock in pickle.Open:
        ohlc = pd.DataFrame({
                                "Open": pickle.Open[stock], "High": pickle.High[stock], "Low": pickle.Low[stock],
                                "Close": pickle.Close[stock], "Volume": pickle.Volume[stock]
                            })

        mpf.plot(ohlc, type='candle', mav=(20, 100), volume=True, title=stock, style='blueskies')



