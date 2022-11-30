import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
import glob



def isolate_time_period(x, date_time, initial_date, final_date):
    """
    Description
    -----------
        Takes an array of data and returns a pandas date-time
            and signal values over specified date range.

    Parameters
    ----------
        x : data to be processed
        data_time : a pandas date time object, describing the time
            stamps associated with x
        initial_date : string, first data in the time period that we're
            interested in, in the format 'dd/mm/yy'
        final_date : string, final data in the time period that we're
            interested in, in the format 'dd/mm/yy'

    Returns
    -------
        x_new : signal amplitude over the specified date range
        date_time_new : pandas date time over the specified date range
    """

    # Check that initial_date and final_date are strings
    assert isinstance(initial_date, str)
    assert isinstance(final_date, str)

    # Date range we're interested in
    initial_date_time = pd.to_datetime(initial_date, dayfirst=True)
    final_date_time = pd.to_datetime(final_date, dayfirst=True)

    # Boolean array showing indices where date range occurs
    i_range = (date_time > initial_date_time) & (date_time < final_date_time)

    # Outputs
    date_time_new = date_time[i_range]
    x_new = x[i_range]

    # Stop processing data if data is outside the chosen time period
    if len(x_new) == 0:
        print('data outside the selected time period')
        exit()

    return x_new, date_time_new



def low_pass_filter(x, wn=0.01, order=3):
    """
    Description
    -----------
        Passes data through low-pass filter, using filtfilt so that no
            phase difference is induced.

    Parameters
    ----------
        x : signal to be filtered
        wn : normalised cut-off frequency
        order : order of  the filter

    Returns
    -------
        x_filt : the filtered signal
    """

    from scipy.signal import butter, filtfilt

    b, a = butter(N=order, Wn=wn)
    x_filt = filtfilt(b, a, x)

    return x_filt


def high_pass_filter(x):
    """
    Description
    -----------
        Passes data through high-pass filter, using filtfilt so that no
            phase difference is induced.

    Parameters
    ----------
        x : signal to be filtered

    Returns
    -------
        x_filt : the filtered signal
    """

    from scipy.signal import butter, filtfilt

    b, a = butter(N=3, Wn=0.01, btype='highpass')
    x_filt = filtfilt(b, a, x)

    return x_filt


def convert_to_seconds(date_time, ff_date_time):
    """
    Description
    -----------
        Converts the date-time associated with x into the
            number of seconds since the start of the furnace
            fault data that we are interested in. Also converts
            the furnace fault data into seconds.

    Parameters
    ----------
        date_time : pandas date time associated with x
        ff_date_time : pandas date time associated with
            furnace faults

    Returns
    -------
        x_ts : total seconds associated with signal x
        ff_ts : total seconds associated with furnace faults
    """

    # Time delta between date_time and the start of the date_time associated
    # with the furnace faults.
    x_ts = (pd.to_timedelta(date_time - ff_date_time.iloc[0]).
            dt.total_seconds())
    ff_ts = (pd.to_timedelta(ff_date_time - ff_date_time.iloc[0]).
             dt.total_seconds())

    return x_ts, ff_ts


def interpolate(x, x_ts, ff_ts, tag_name=None, tag_ID=None, plot=False,
                kind='linear'):
    """
    Description
    -----------
        Interpolates to get estimates of x at the furnace fault
            time stamps. Interpolation is conducted using the
            previous value.

    Parameters
    ----------
        x : signal input
        x_ts : total seconds associated with signal x
        ff_ts : total seconds associated with furnace fault signal
        tag_name : String of the tag name. Is only needed if we are
            going to create a plot.
        tag_ID : String of tag ID. Is only needed if we are going to
            create a plot.
        plot : boolean value stating whether or not we will plot the result

    Returns
    -------
        x_int : interpolated x values
    """

    from scipy.interpolate import interp1d

    f = interp1d(x_ts, x, kind, fill_value='extrapolate')
    x_int = f(ff_ts)

    if plot:
        fig, ax = plt.subplots()
        ax.plot(x_ts, x, color='black', marker='.', label='Original')
        ax.plot(ff_ts, x_int, color='red', marker='.',
                label='Interpolated')
        title = '(interpolation)'
        ax.set_title(title)
        ax.legend()

    return x_int


def standardise(x, offset, width):
    """
    Description
    -----------
        Standardise the array, x, so that it removes 'offset' then divides
            by 'width'.

    Parameters
    ----------
        x : signal to be standardised
        offset : fairly obvious...
        width : also fairly obvious...

    Returns
    -------
        xs : standardised signal
    """

    if width == 0:
        print('Warning: standard deviation equal to zero')
        xs = x - offset
    else:
        xs = (x - offset) / width

    return xs


def remove_spikes(x, tag_name=None, tag_ID=None, plot=False, olr_def=3):
    """
    Description
    -----------
        Removes outlier spikes from the data x and replaces resulting
            missing values using linear interpolation. We pass
            the signal through a high-pass filter before it gets to
            this point to remove slowly varying trends. Padding is also
            required, due to the assumption that the signal dies away to
            zero outside of the range we are interested in.

    Parameters
    ----------
        x : signal to be processed
        tag_name : String of the tag name. Is only needed if we are
            going to create a plot.
        tag_ID : String of tag ID. Is only needed if we are going to
            create a plot.
        plot : option to plot results of outlier removal
        olr_der : no. of standard deviations beyond the mean that will
            be defined as an outlier

    Returns
    -------
        x_final : x with spikes removed and replaced with data from
            linear interpolation
    """

    # Pad the beginning and end of x with median of signal before filtering
    x = np.append(np.median(x), x)
    x = np.append(x, np.median(x))

    # Pass through high pass filter to remove slowly varying trends
    x_filt = high_pass_filter(x, tag_name, tag_ID, False)

    # Mean and standard deviation of filtered signal
    m = np.mean(x_filt)

    # Remove mean from filtered signal
    xn = x_filt - m

    # Remove first and last elements of all signals (the zero-padding)
    x_filt = x_filt[1 : -1]
    xn = xn[1 : -1]
    x = x[1 : -1]

    # Standard deviation of mean-normalised signal
    s = np.std(xn)

    # Here we define outlier as being more than olr_def standard
    # deviations from the mean
    spike_locations = np.where(np.abs(xn) > olr_def * s)[0]
    indx = np.arange(0, len(x))
    indx_no_spikes = np.delete(indx, spike_locations)

    x_no_spikes = np.delete(x, spike_locations)
    x_final = np.interp(indx, indx_no_spikes, x_no_spikes)

    if plot:
        fig, ax = plt.subplots(nrows=2)

        # Plot outliers on filtered signal
        ax[0].plot(indx, x_filt, color='black', label='Filtered signal')
        ax[0].plot(spike_locations, x_filt[spike_locations], 'o',
                   color='red', label='Outliers')
        title = tag_ID + ' ' + tag_name + '\n' + '(spike removal)'
        ax[0].set_title(title)
        ax[0].legend()

        # Plot outliers on original signal
        ax[1].plot(indx, x, color='black', label='Original signal')
        ax[1].plot(spike_locations, x[spike_locations], 'o',
                   color='red', label='Outliers')
        ax[1].plot(indx, x_final, color='blue', label='Remaining signal')
        ax[1].legend()

        plt.tight_layout()

    return x_final
