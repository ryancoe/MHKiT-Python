import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
from mhkit.wave.resource import significant_wave_height as _sig_wave_height
from mhkit.wave.resource import peak_period as _peak_period
from mhkit.river.graphics import _xy_plot


def plot_spectrum(S, ax=None):
    """
    Plots wave amplitude spectrum versus omega
    
    Parameters
    ------------
    S: pandas DataFrame
        Spectral density [m^2/Hz] indexed frequency [Hz]
    ax : matplotlib axes object
        Axes for plotting.  If None, then a new figure is created.
    Returns
    ---------
    ax : matplotlib pyplot axes
    
    """
    assert isinstance(S, pd.DataFrame), 'S must be of type pd.DataFrame'
    
    f = S.index
    
    ax = _xy_plot(f*2*np.pi, S/(2*np.pi), fmt='-', xlabel='omega [rad/s]', 
             ylabel='Spectral density [m$^2$s/rad]', ax=ax)
    
    """
    spectrum_type = S.columns
    if S.shape[1] == 1:
        Hm0 = _sig_wave_height(S).iloc[0,0]
        Tp0 = _peak_period(S).iloc[0,0]
        title = 'Spectrum: ' + spectrum_type[0] + ' \n Tp = {:0.2f}, Hs = {:0.2f}'.format(Tp0,Hm0)
        ax.set_title(title)
    else:
        ax.legend(spectrum_type)
    """   
    return ax

def plot_elevation_timeseries(eta, ax=None):
    """
    Plot wave surface elevation time-series
    
    Parameters
    ------------
    eta: pandas DataFrame
        Wave surface elevation [m] indexed by time [datetime or s]
    ax : matplotlib axes object
        Axes for plotting.  If None, then a new figure is created.
        
    Returns
    ---------
    ax : matplotlib pyplot axes
            
    """
    
    assert isinstance(eta, pd.DataFrame), 'eta must be of type pd.DataFrame'
    
    ax = _xy_plot(eta.index, eta, fmt='-', xlabel='Time', 
                  ylabel='$\eta$ [m]', ax=ax)
    
    return ax

def plot_matrix(M, xlabel='Te', ylabel='Hm0', zlabel=None, show_values=True, 
                ax=None):
    """
    Plots values in the matrix as a scatter diagram

    Parameters
    ------------
    M: pandas DataFrame
        Matrix with numeric labels for x and y axis, and numeric entries.
        An example would be the average capture length matrix generated by
        mhkit.device.wave, or something similar.
    xlabel: string (optional)
        Title of the x-axis
    ylabel: string (optional)
        Title of the y-axis
    zlabel: string (optional)
        Colorbar label
    show_values : bool (optional)
        Show values on the scatter diagram
    ax : matplotlib axes object
        Axes for plotting.  If None, then a new figure is created.
    
    Returns
    ---------
    ax : matplotlib pyplot axes
    
    """
    assert isinstance(M, pd.DataFrame), 'M must be of type pd.DataFrame'
    
    if ax is None:
        plt.figure()
        ax = plt.gca()
        
    im = ax.imshow(M, origin='lower', aspect='auto')
    
    # Add colorbar
    cbar = plt.colorbar(im)
    if zlabel:
        cbar.set_label(zlabel, rotation=270, labelpad=15)
    
    # Set x and y label
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    
    # Show values in the plot
    if show_values:
        for i, col in enumerate(M.columns):
            for j, index in enumerate(M.index):
                if not np.isnan(M.loc[index,col]):
                    ax.text(i, j, format(M.loc[index,col], '.2f'), ha="center", va="center")
    
    # Reset x and y ticks
    ax.set_xticks(np.arange(len(M.columns)))
    ax.set_yticks(np.arange(len(M.index)))
    ax.set_xticklabels(M.columns)
    ax.set_yticklabels(M.index)

    return ax

def plot_chakrabarti(H, lambda_w, D, ax=None):
    """
    Plots, in the style of Chakrabart (2005), relative importance of viscous, 
    inertia, and diffraction phemonena

    Chakrabarti, Subrata. Handbook of Offshore Engineering (2-volume set). 
    Elsevier, 2005.

    Parameters
    ------------    
    H: float or numpy array or pandas Series
        Wave height [m]   
    lambda_w: float or numpy array or pandas Series
        Wave length [m]
    D: float or numpy array or pandas Series
        Characteristic length [m]
    ax : matplotlib axes object (optional)
        Axes for plotting.  If None, then a new figure is created.
    
    
    Returns
    ---------
    ax : matplotlib pyplot axes

    Examples
    --------
    **Using floats**

    >>> plt.figure()
    >>> D = 5
    >>> H = 8
    >>> lambda_w = 200
    >>> wave.graphics.plot_chakrabarti(H, lambda_w, D)

    **Using numpy array**
    
    >>> plt.figure()
    >>> D = np.linspace(5,15,5)
    >>> H = 8*np.ones_like(D)
    >>> lambda_w = 200*np.ones_like(D)
    >>> wave.graphics.plot_chakrabarti(H, lambda_w, D)

    **Using pandas DataFrame**

    >>> plt.figure()
    >>> D = np.linspace(5,15,5)
    >>> H = 8*np.ones_like(D)
    >>> lambda_w = 200*np.ones_like(D)
    >>> df = pd.DataFrame([H.flatten(),lambda_w.flatten(),D.flatten()], \
                              index=['H','lambda_w','D']).transpose()
    >>> wave.graphics.plot_chakrabarti(df.H, df.lambda_w, df.D)
    """

    assert isinstance(H, (np.ndarray, float, int, np.int64,pd.Series)), 'H must be a real numeric type'
    assert isinstance(lambda_w, (np.ndarray, float, int, np.int64,pd.Series)), 'lambda_w must be a real numeric type'
    assert isinstance(D, (np.ndarray, float, int, np.int64,pd.Series)), 'D must be a real numeric type'
    
    if any([(isinstance(H, np.ndarray) or isinstance(H, pd.Series)),        \
            (isinstance(lambda_w, np.ndarray) or isinstance(H, pd.Series)), \
            (isinstance(D, np.ndarray) or isinstance(H, pd.Series))\
           ]):
        errMsg = 'H, lambda_w, and D must be same shape'
        n_H = H.squeeze().shape
        n_lambda_w = lambda_w.squeeze().shape
        n_D = D.squeeze().shape
        assert n_H == n_lambda_w and n_H == n_D, errMsg
        
        if isinstance(H, np.ndarray):
            mvals = pd.DataFrame(H.reshape(len(H),1), columns=['H'])
            mvals['lambda_w'] = lambda_w
            mvals['D'] = D
        elif isinstance(H, pd.Series):   
            mvals = pd.DataFrame(H )
            mvals['lambda_w'] = lambda_w
            mvals['D'] = D 

    else:        
        H = np.array([H])
        lambda_w = np.array([lambda_w])
        D = np.array([D])
        mvals = pd.DataFrame(H.reshape(len(H),1), columns=['H'])
        mvals['lambda_w'] = lambda_w
        mvals['D'] = D
                
    if ax is None:
        plt.figure()
        ax = plt.gca()

    ax.set_xscale('log')
    ax.set_yscale('log')
    x = np.logspace(-2, 1, 1000)

    # upper bound of low drag region    
    ldv = 20
    y_small_drag = ldv*np.ones_like(x)
    ax.plot(x[x < 0.14 * np.pi / ldv], y_small_drag[x < 0.14 * np.pi / ldv],
            'k--')
    ax.text(0.0125, 30, 'drag', ha='center', va='top', fontstyle='italic',
            fontsize='small')

    # upper bound of small drag region
    sdv = 1.5
    y_small_drag = sdv*np.ones_like(x)
    ax.plot(x[x < 0.14 * np.pi / sdv], y_small_drag[x < 0.14 * np.pi / sdv],
            'k--')
    ax.text(0.02, 7, 'inertia \n& drag', ha='center', va='top',
            fontstyle='italic', fontsize='small')
     
    # upper bound of neglible drag region   
    ndv = 0.25
    y_small_drag = ndv*np.ones_like(x)
    ax.plot(x[x < 0.14 * np.pi / ndv], y_small_drag[x < 0.14 * np.pi / ndv],
            'k--')
    ax.text(8e-2, 0.7, 'large\ninertia', ha='center', va='top',
        fontstyle='italic', fontsize='small')

    ax.text(8e-2, 6e-2, 'all\ninertia', ha='center', va='top',
            fontstyle='italic', fontsize='small')

    # left bound of diffraction region
    drv = 0.5
    y_diff_reg = np.array([1e-2, 0.14 * np.pi / drv])
    x_diff_reg = 0.5 * np.ones_like(y_diff_reg)
    ax.plot(x_diff_reg, y_diff_reg, 'k--')
    ax.text(2, 6e-2, 'diffraction', ha='center', va='top', fontstyle='italic',
            fontsize='small')

    # deep water breaking limit (H/lambda_w = 0.14)
    y_breaking = 0.14 * np.pi / x
    ax.plot(x, y_breaking, 'k-')
    ax.text(1, 7, 'wave\nbreaking\n$H/\lambda_w > 0.14$', ha='center', va='top',
            fontstyle='italic', fontsize='small')

    for index, row in mvals.iterrows():
        xx = row['H']/row['D']
        yy = np.pi*row['D']/row['lambda_w']
        lab = '$H = %.2g,\\,$lambda_{w}$ = %.2g,\\,D = %.2g$' % (row['H'], row['lambda_w'], row['D'])
        ax.plot(xx, yy, 'o', label=lab)
        # print(row['c1'], row['c2'])

    if index > 0:
        ax.legend(fontsize='xx-small', ncol=2)

    ax.set_xlim((0.01, 10))
    ax.set_ylim((0.01, 50))

    ax.set_xlabel('Diffraction parameter, $\\frac{\\pi D}{\\lambda_w}$')
    ax.set_ylabel('KC parameter, $\\frac{H}{D}$')

    plt.tight_layout()
