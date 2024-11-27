#!/usr/bin/env python
# coding: utf-8


from typing import List
from pathlib import Path
import os
import json
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.ndimage import sobel, gaussian_filter
from scipy.signal import find_peaks
from scipy.optimize import curve_fit

from chars import greek, phys



# N=75

cwd = Path(os.getcwd())

results_top_dir = cwd / "WS2_Grating_Eamonn" / "Results" / 'WS₂, SiO₂, Si 5'

# results_dir = cwd / "WS2_Grating_Eamonn" / "Results" / 'WS₂, SiO₂, Si' / 't=18.0nm Λ=500nm FF=0.84 N=75' / 'data'
# results_dir = cwd / "WS2_Grating_Eamonn" / "Results" / 'WS₂, SiO₂, Si 4' / 't=60.0nm Λ=350nm FF=0.55 N=75' / 'data'
# results_dir = cwd / "WS2_Grating_Eamonn" / "Results" / 'WS₂, SiO₂, Si' / 't=38.0nm Λ=500nm FF=0.76 N=75' / 'data'
# results_dir = cwd / "WS2_Grating_Eamonn" / "Results" / 'WS₂, SiO₂, Si 4' / 't=20.0nm Λ=550nm FF=0.55 N=75' / 'data'


savepath = cwd / 'mode_fitting'
savepath.mkdir(exist_ok=True, parents=True)



sims = sorted(os.listdir(results_top_dir))
if 'summary.json' in sims:
    sims.remove('summary.json')
print(len(sims))

sims = [Path(cwd / "WS2_Grating_Eamonn" / "Results" / 'WS₂, SiO₂, Si 5' / 't=80.0nm Λ=600nm FF=0.82 N=75')]

def fit_simulation(results_dir):
    try:
        files = sorted(os.listdir(results_dir))
    except:
        return 0
    file_R = results_dir / files[4]
    file_R_sub = results_dir / files[5]
    print(file_R)

    try:
        N_str = str(results_dir.parents[0]).rsplit('N=')[1]
        N = int(N_str)
    except Exception as e:
        print(f"No N present in file name - {e}")

    R = pd.read_csv(file_R, index_col=0)
    Rsub = pd.read_csv(file_R_sub, index_col=0)

    signalR = (R - Rsub) / Rsub
    signalR = (signalR - np.min(signalR)) / (np.max(signalR) - np.min(signalR))




    lbda_min = 2.2  # y limits in micrometers
    lbda_max = 1.2
    lbda = np.linspace(lbda_min, lbda_max, N)  # Generate wavelengths in micrometers

    N_k=N
    # k_scan=np.linspace(-6.7,6.7,N_k) #mu-1
    kmax=5
    k_scan=np.linspace(-kmax,kmax,N_k) #mu-1
    ky=0.000
    title_name = 'signalR, from R and R_sub CSVs'

    # fig, axs = plt.subplots(1, 1, sharey=True, figsize=(7, 6), dpi=80)
    # pcm = axs.pcolor(k_scan,lbda,signalR,cmap='viridis',clim=(0,1))
    # axs.set(xlabel=f'k$_x$ [{greek.mu}m]',
    #         xlim=(-kmax,kmax),ylim=(lbda_max, lbda_min),
    #         ylabel='Photon Energy [eV]',
    #         title=title_name)
    # # y_eV = 1.45    # reference line at 1.45eV
    # # axs.plot(k_scan,y_eV*k_scan/k_scan,'m--') # reference line at 1.45eV
    # cbar =fig.colorbar(pcm,location='right')
    # cbar.set_label('Reflectivity contrast')
    # plt.minorticks_on()
    # plt.show()



    data_array = np.asarray(signalR)
    sobel_x = sobel(data_array, axis=0)  # Sobel in the x-direction
    sobel_y = sobel(data_array, axis=1)  # Sobel in the y-direction

    sobel_y = sobel(sobel_y, axis=1)  # Sobel in the y-direction

    # Calculate the gradient magnitude (combined Sobel in x and y)
    sobel_magnitude = np.hypot(sobel_x, sobel_y)

    edge_magnitude = np.abs(sobel_y)

    # Normalize edge magnitude for better visualization
    edge_magnitude_normalized = edge_magnitude / np.max(edge_magnitude)

    # Apply Gaussian blur to smooth the edges (adjust sigma as needed for desired blur amount)
    sigma = 0.8
    edge_magnitude_blurred = gaussian_filter(edge_magnitude_normalized, sigma=sigma)


    print(edge_magnitude.shape)

    # fig, axs = plt.subplots(1, 1, sharey=True, figsize=(7, 6), dpi=80)
    # pcm = axs.pcolor(k_scan,lbda,edge_magnitude_blurred,cmap='viridis',clim=(0,1))
    # axs.set(xlabel=f'k$_x$ [{greek.mu}m]',xlim=(-kmax,kmax),ylim=(lbda_max, lbda_min), ylabel='Photon Energy [eV]',title='Edge detection, 2x sobel axis=1')
    # # y_eV = 1.45    # reference line at 1.45eV
    # # axs.plot(k_scan,y_eV*k_scan/k_scan,'m--') # reference line at 1.45eV
    # cbar =fig.colorbar(pcm,location='right')
    # cbar.set_label('Reflectivity contrast')
    # plt.minorticks_on()
    # plt.savefig(savepath / 'edgedetect_gaussian.png', dpi=150)
    # plt.show()




    # find the coords of above and below the top mode, identify the gap
    # line_y_max = [np.max(row)*np.mean(row)/np.sum(row) for row in edge_magnitude_normalized]
    # Assuming edge_magnitude_normalized is already defined

    # Calculate the central position based on whether N is even or odd
    central_position = N // 2 if N % 2 != 0 else (N // 2) - 1

    # Calculate the range to exclude (5% of N)
    exclude_range = int(0.05 * N)

    # Now compute line_y_max by excluding pixels within 5% of the central position for each row
    line_y_max = []
    for row in edge_magnitude_normalized:
        # Create a mask to exclude pixels within 5% of the central position
        mask = (np.arange(N) < central_position - exclude_range) | (np.arange(N) > central_position + exclude_range)

        try:
            # Apply the mask to the row
            filtered_row = row[mask]
        except IndexError:
            print("WRONG N - DEBUG")
            time.sleep(5)
            return 0

        # Compute the value for this row and append to the result
        if len(filtered_row) > 0:  # Make sure there are still data points after masking
            result = np.max(filtered_row) * np.mean(filtered_row) / np.sum(filtered_row)
            line_y_max.append(result)
        else:
            # If no values remain after the mask, append a default value (e.g., NaN or zero)
            line_y_max.append(np.nan)

    # Now line_y_max contains the processed values


    pd_line_y_max = pd.Series(line_y_max)

    # Apply a 3-point moving average to smooth the data
    series_ymax_mavg = pd_line_y_max.rolling(window=6, center=True).mean()


    # Use the Series index as x values
    y = series_ymax_mavg
    x = series_ymax_mavg.index
    y = y.fillna(0)

    y_min, y_max = y.min(), y.max()
    # Define thresholds
    trough_threshold = y_min + 0.4 * (y_max - y_min)  # Troughs must be below
    peak_threshold = y_min + 0.4 * (y_max - y_min)   # Peaks must be above

    # Filter peaks and troughs based on thresholds
    peaks, _ = find_peaks(y)
    normalised_peaks = [(y[p]-y_min)/(y_max-y_min) for p in peaks]

    print(f"PEAKS: {peaks}")
    peaks = np.array([int(p) for p in peaks if y[p] >= peak_threshold])  # Keep only valid peaks
    print(f"PEAKS: {peaks}")
    try:
        peaks[0]
    except:
        print("No peaks")
        return 0

    troughs, _ = find_peaks(-y)  # Invert y to find minima

    print(f"TROUGHS: {troughs}")
    troughs = np.array([int(t) for t in troughs if y[t] <= trough_threshold])  # Keep only valid troughs
    troughs = np.append(troughs, N-2)
    print(f"TROUGHS: {troughs}")
    # print(y[-1:])

    print(type(troughs), type(peaks))
    # peaks_df = pd.Series(peaks)
    # troughs_df = pd.Series(troughs)
    # pt_df = pd.DataFrame({'peaks':peaks_df, 'troughs':troughs_df})
    # print(pt_df)

    minima_indices = troughs
    min_peak_trough_diff = 0.4

    max_peak = {} # [loc, comparable diff]
    # min_troughs = [] # [loc1, loc2]

    for _,peak in enumerate(peaks):
        before_trough = troughs[troughs < peak].max() if (troughs < peak).any() else None
        after_trough = troughs[troughs > peak].min() if (troughs > peak).any() else None

        if None in [before_trough, after_trough]:
            continue
        before_trough = int(before_trough)
        after_trough = int(after_trough)

        diff1, diff2 = y[peak] - y[before_trough], y[peak] - y[after_trough]
        diff_min = np.min([diff1, diff2]) # find min proximity in y to trough

        # if max_peak == None or max_peak[1] < diff_min:
        # max_peak.append([peak,diff_min])
        # min_troughs.append([before_trough, after_trough])

        max_peak[f'{peak}'] = [diff_min, before_trough, after_trough]

        print(f"Peak at {peak} - before={before_trough}, after={after_trough}, diff {diff_min}")

    if len(max_peak) == 0:
        return 0

    max_peak_sorted = dict(sorted(max_peak.items(), key=lambda item: item[1][0], reverse=True))

    peak_indices_sorted = list(max_peak_sorted.keys())
    compare_troughs = []
    # remove if different peak of same troughs
    for i in range (0, len(peak_indices_sorted)):
        locs = max_peak_sorted[peak_indices_sorted[i]][1:]
        if locs in compare_troughs:
            del max_peak_sorted[peak_indices_sorted[i]]
        compare_troughs.append(max_peak_sorted[peak_indices_sorted[i]])

    try:
        print(f"Found peaks at {max_peak_sorted.keys()}")
    except:
        print(f"Error with peaks, {max_peak_sorted}")
        return 0

    for i in range(0, len(peak_indices_sorted)):
        diff = max_peak_sorted[peak_indices_sorted[i]][0]
        if diff < (y_max - y_min)*min_peak_trough_diff:
            print("No definative modes found using max of each row, looking at peaks/troughs.")
            return 0




    # Step 5: Plot the results
    plt.figure(figsize=(12, 6))
    plt.plot(x, y, label='Data', color='lightgray')
    plt.scatter(x[peaks], y[peaks], color='red', label='Maxima')
    plt.scatter(x[minima_indices], y[minima_indices], color='blue', label='Minima', zorder=5)

    for p in peak_indices_sorted:
        p_ = int(p)
        plt.scatter(x[p_], y[p_], color='green', label='Peak', s=100, zorder=10)
        plt.scatter([x[max_peak_sorted[p][1]], x[max_peak_sorted[p][2]]], [y[max_peak_sorted[p][1]], y[max_peak_sorted[p][2]]], color='purple', label='Neighbouring troughs', s=100, zorder=10)

    plt.axhline(y=peak_threshold)
    plt.axhline(y=trough_threshold)
    plt.title('Identifying Minima near the Tallest Distinct Peak')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.grid()

    plt.savefig(savepath / 'peaks.png', dpi=150)
    plt.show()




    # Define the hyperbolic asymptotic model for curve fitting
    def hyperbola_asymptotic_u(x, a, L, M, F, B, V, c):
        """
        Hyperbolic asymptotic fit model
        :param x: x
        :param a: shift y
        :param b: shift x (redundant, =N/2)
        :param L: multiply y
        :param M: multiply x
        :param F: pointyness
        :param B: asymptote in y
        :param sign: u or n shape (redundant)
        :return: g(x) func result
        """
        nonlocal N
        sign = -1 * c
        xbM = ((x - N/2) ** 2) / M
        f_x = sign*np.sqrt(np.abs( (F + xbM) ))
        g_x = a + ( f_x / (V*( 1 + (np.abs(f_x) / B) )) )
        return g_x * L

    def hyperbola_asymptotic_n(x, a, L, M, F, B, V, c):
        """
        Hyperbolic asymptotic fit model
        :param x: x
        :param a: shift y
        :param b: shift x (redundant, =N/2)
        :param L: multiply y
        :param M: multiply x
        :param F: pointyness
        :param B: asymptote in y
        :param sign: u or n shape (redundant)
        :return: g(x) func result
        """
        nonlocal N
        sign = 1 * c
        xbM = ((x - N/2) ** 2) / M
        f_x = sign*np.sqrt(np.abs( (F + xbM) ))
        g_x = a + ( f_x / (V*( 1 + (np.abs(f_x) / B) )) )
        return g_x * L

    hyperbolas = [hyperbola_asymptotic_u, hyperbola_asymptotic_n]

    def graph_to_fitted(array: list | float, N: int = N) -> list | float:
        """
        Convert energy values (eV) to pixel coordinates/positions given a 1.2-2.2 eV range with N length square dimension array.
        :param array: list or single number (energy values)
        :return: new list or number (pixel positions)
        """
        max_energy, min_energy = 2.2, 1.2
        min_pixel, max_pixel = 0, N
        pixel = -(array - max_energy) * (max_pixel-min_pixel) / (max_energy-min_energy) + min_pixel
        return pixel


    fitting_data = {}

    def process_fitting(iteration, y_min, y_max, sign):
        hyperbola_asymptotic = hyperbolas[int(iteration%2)] # decide u or n shape

        # Create a heatmap (visualization)
        # plt.figure(figsize=(10, 6), dpi=80)
        # sns.heatmap(edge_magnitude_normalized, cmap='viridis', xticklabels=False, yticklabels=False, alpha=0.5)
        #
        # # Add horizontal lines at the minimum troughs
        # plt.axhline(y=min_troughs[0], color='black', linestyle='--', label='Mode max/min')
        # plt.axhline(y=min_troughs[1], color='black', linestyle='--')

        # Extract the region of interest between the minimum troughs

        data_region = edge_magnitude_normalized[y_min:y_max, :]
        x_indices = np.arange(data_region.shape[1])

        # Calculate weighted average energy positions for the top 25 quantile values
        y_positions = []
        for x in x_indices:
            column = data_region[:, x]
            y_indices = np.arange(len(column))

            quantile_threshold = np.percentile(column, 95)
            filtered_indices = np.where(column >= quantile_threshold)[0]
            filtered_column = column[filtered_indices]
            filtered_y_indices = y_indices[filtered_indices]

            if np.sum(filtered_column) > 0:
                weighted_avg = np.sum(filtered_column * filtered_y_indices) / np.sum(filtered_column)
                y_positions.append(weighted_avg + y_min)
            else:
                y_positions.append((y_max + y_min) / 2)

        x_data = np.array(x_indices)
        y_data = np.array(y_positions)

        if len(y_data) % 2 == 1:  # Odd number of points
            central_value = y_data[len(y_data) // 2]
        else:  # Even number of points, use average of the two middle values
            mid_idx = len(y_data) // 2
            central_value = np.max([y_data[mid_idx - 1], y_data[mid_idx]])

        # Remove data points
        max_energy_pixel = int(graph_to_fitted(2))
        if iteration == 0:
            mask = (y_data <= central_value) & (y_data >= max_energy_pixel)
            x_data = x_data[mask]
            y_data = y_data[mask]
        elif iteration == 1:
            mask = (y_data >= central_value) & (y_data >= max_energy_pixel)
            x_data = x_data[mask]
            y_data = y_data[mask]

        print(np.shape(y_data), np.shape(x_data))
        if float(len(x_data)) < N*0.7:
            print("Not enough data. Skipping.")
            return 0


        initial_guess = \
            [0.3, 7000, 0.6, 500, 0.3, 5, 0.1] # a = 0.0797, b = 37.5000, L = 6999.9990, M = 0.6000, F = 500.0000, B = 0.3863, V = 4.9998, c=0.1
        bounds = \
            ([-50, 100, 0.5, 1, 0, 1, -1],
             [50, 10000, 10, 10000, 100, 20, 1])

        # Perform hyperbolic curve fitting

        popt, pcov = curve_fit(f=hyperbola_asymptotic, xdata=x_data, ydata=y_data, p0=initial_guess, bounds=bounds, maxfev=10000)

        # Generate smooth x-values for plotting the fitted hyperbolic curve
        x_plotting = np.linspace(0, data_region.shape[1] - 1, 300)
        # y_fit = hyperbola_asymptotic(x_plotting, *popt)

        # Calculate residuals and identify outliers
        residuals = y_data - hyperbola_asymptotic(x_data, *popt)
        threshold = 2 * np.std(residuals)
        outlier_indices = np.abs(residuals) > threshold
        x_data_cleaned = x_data[~outlier_indices]
        y_data_cleaned = y_data[~outlier_indices]


        initial_guess_2 = popt

        # Refit the hyperbolic model to the cleaned data
        popt_cleaned, pcov_cleaned = curve_fit(hyperbola_asymptotic, x_data_cleaned, y_data_cleaned, p0=initial_guess_2, bounds=bounds, maxfev=10000)
        y_fit_cleaned = hyperbola_asymptotic(x_plotting, *popt_cleaned)
        # print(f"PCOV cleaned: {pcov_cleaned}")

        # Overlay the data and the fitted hyperbolic curve on the heatmap
        # plt.plot(x_data, y_data, 'bx', markersize=6, label='Weighted Avg')
        # plt.plot(x_data_cleaned, y_data_cleaned, 'bo', markersize=6, label='Weighted Avg cleaned')
        # # plt.plot(x_plotting, y_fit, 'r--', linewidth=2, label='Initial Fit')
        # plt.plot(x_plotting, y_fit_cleaned, 'r-', linewidth=2, label='Refitted Hyperbolic Curve')

        # plt.xlabel('k_x')
        # plt.ylabel('eV')
        # if iteration == 0:
        #     plt.legend(loc='lower center')
        # if iteration == 1:
        #     plt.legend(loc='upper center')
        #
        # plt.title('Asymptotic hyperbola fit')
        # plt.savefig(savepath / f'Fitted {iteration}.png', dpi=150)
        # plt.show()

        a_cleaned, L_cleaned, M_cleaned, F_cleaned, B_cleaned, V_cleaned, ex = popt_cleaned
        print(f"Fitted parameters (cleaned hyperbolic):\na = {a_cleaned:.4f}, L = {L_cleaned:.4f}, M = {M_cleaned:.4f}, F = {F_cleaned:.4f}, B = {B_cleaned:.4f}, V = {V_cleaned:.4f}")


        residuals = y_data - hyperbola_asymptotic(x_data, *popt_cleaned)
        rmse = np.sqrt(np.mean(residuals**2))
        ss_total = np.sum((y_data - np.mean(y_data))**2)
        ss_residual = np.sum(residuals**2)
        r2 = 1 - (ss_residual / ss_total)
        print(f"\n\nRMSE: {rmse}, R^2: {r2}")

        r2_threshold = 0.6
        print(f"EVALUATING {abs(r2):.4f} vs {r2_threshold:.2f}")
        if float(abs(r2)) > float(r2_threshold):
            print("WELL FITTED")
            fitting_data[str(iteration)] = {'R2': float(r2), 'popt': popt_cleaned.tolist()}
            return 1
        else:
            return 0



    # y_min, y_max = min_troughs[1], None
    # y_min, y_max = min_troughs[0], min_troughs[1]
    # if len(min_troughs) == 2:
    #     min_troughs.append(None)
    #     print(min_troughs)

    results = {}


    # loop - 0 upper, 1 lower
    # sign - upper -1, lower 1
    for i in [0,1,2,3,4,5]:
        # print(i)
        trough_idxs = [max_peak_sorted[key][1:] for key in max_peak_sorted.keys()]
        y_min_1 = trough_idxs[0][0]
        y_max_1 = trough_idxs[0][1]

        fit_remainder = False
        try:
            y_min_2 = trough_idxs[1][0]
            y_max_2 = trough_idxs[1][1]
        except:
            y_min_3 = y_max_1
            y_max_3 = int(N * 0.95)

            if (y_max_3 - y_min_3) <= N * 0.1:
                continue
            fit_remainder = True

        if i==0:
            print("MODE 0")
            try:
                result = process_fitting(i, y_min_1, y_max_1, -1)
                results[str(i)] = result
            except ValueError:
                result = 0


        elif (i==1) and (results['0']==0):
            print("MODE 1 - UPPER MODE NOT FITTED, LOOKING FOR LOWER MODE INSTEAD")
            try:
                result = process_fitting(i, y_min_1, y_max_1, 1)
                results[str(i)] = result
            except ValueError:
                result = 0


        elif (i==2) and (results['0']==0) and (not fit_remainder):
            print("MODE 2")
            try:
                result = process_fitting(i, y_min_2, y_max_2, -1)
                results[str(i)] = result
            except ValueError:
                result = 0


        elif (i==3) and (results['0']==1) and (not fit_remainder):
            print("MODE 3")
            try:
                result = process_fitting(i, y_min_2, y_max_2, 1)
                results[str(i)] = result
            except ValueError:
                result = 0


        elif (i == 4) and (fit_remainder):
            print("MODE 4")
            try:
                result = process_fitting(i, y_min_3, y_max_3, -1)
                results[str(i)] = result
            except ValueError:
                result = 0


        elif (i == 5) and (fit_remainder):
            print("MODE 5")
            try:
                result = process_fitting(i, y_min_3, y_max_3, 1)
                results[str(i)] = result
            except ValueError:
                result = 0




        print(f"******** RESULT ********\n{results}")




    if len(results) >= 2:
        print(f"{len(results)} modes present and well fitted")
    if len(results) == 0:
        print("No modes fitted")
        # print(fitting_data)
        fitting_data = {}
        return 0
    else:
        print(f"Modes NOT present - {len(results)} modes fitted")


    print(fitting_data)




    def fitted_to_graph(array: list | float, N: int = N) -> list | float:
        """
        Convert pixel coords/positions to eV given 1.2, 2.2 range, with N length square dimension array
        :param array: list or single number
        :return: new list or number
        """
        max_energy, min_energy = 2.2, 1.2
        min_pixel, max_pixel = 0, N
        energy_values = max_energy - (array - min_pixel) * (max_energy - min_energy) / (max_pixel - min_pixel)
        return energy_values



    k_scan_line = np.linspace(-kmax, kmax, 300)
    x_graphing = np.linspace(0, N+1, 300)
    k_scan = np.linspace(-kmax, kmax, N)

    fig, axs = plt.subplots(1, 1, sharey=True, figsize=(7, 6), dpi=80)
    pcm = axs.pcolor(k_scan,lbda,signalR,cmap='viridis',clim=(0,1))
    m1 = r'{-1}'
    axs.set(xlabel=f'k$_x$ [{greek.mu}m{m1}]',xlim=(-kmax,kmax),ylim=(lbda_max, lbda_min), ylabel='Photon Energy [eV]',
            title=f'Upper and lower modes, vertices, asymptotes\n{results_dir.parents[0].name}')
    # y_eV = 1.45    # reference line at 1.45eV
    # axs.plot(k_scan,y_eV*k_scan/k_scan,'m--') # reference line at 1.45eV
    cbar =fig.colorbar(pcm,location='right')
    cbar.set_label('Reflectivity contrast')
    plt.minorticks_on()

    fits = []
    vertices = []
    asyms = []
    for i in [0,1,2,3,4,5]:
        try:
            popt = fitting_data[f'{i}']['popt']
            fit = hyperbolas[i%2](x_graphing, *popt)
            plt.plot(k_scan_line, fitted_to_graph(fit), 'r-', linewidth=2, label='Fit')
            fits.append(fit)

            vertex = fitted_to_graph(hyperbolas[i%2](N/2, *popt))
            asym = fitted_to_graph(hyperbolas[i%2](1e9, *popt))

            vertices.append(vertex)
            asyms.append(asym)

            plt.axhline(y=vertex, color='m', linestyle='--', label='Vertex')
            plt.axhline(y=asym, color='k', linestyle=':', label='Asymptote', linewidth=3)
        except:
            print(f"MODE NOT FOUND FOR i={i}")
            continue


    print(f"Vertices {np.array(vertices).tolist()}\nAsyms {np.array(asyms).tolist()}")

    plt.axhline(y=1.8,color='c', linestyle=':', linewidth=3, label='1.8eV')


    plt.legend(loc='upper left', framealpha=0.8)
    plt.savefig(savepath / 'Fitted modes.png', dpi=150)
    plt.show()



    # for i in [0,1]:
    #     try:
    #         plt.axhline(y=vertices[i], color='m', linestyle='--', label='Vertex')
    #
    #         plt.axhline(y=asyms[i], color='k', linestyle=':', label='Asymptote', linewidth=3)
    #
    #         plt.plot(k_scan_line, fitted_to_graph(fits[i]), 'r-', linewidth=2, label='Fit')
    #     except:
    #         continue




    fitting_results = {'vertices':vertices, 'asyms':asyms}

    fitting_summary_single = {}
    fitting_summary_single['fitting info'] = fitting_data
    fitting_summary_single['fitting results'] = fitting_results
    fitting_summary_multi[f'{results_dir.parents[0].name}'] = fitting_summary_single

    print(fitting_summary_single)
    print(f"Simulation fitted - {sim}")

    # plt.clf()
    time.sleep(1)


fitting_summary_multi = {}

for int_loc, sim in enumerate(sims):
    sim = Path(sim)
    # print(sim / 'data')
    results_dir = results_top_dir / sim / 'data'
    # print(results_dir)
    # print(results_top_dir)
    print(f"***\nSim no. {int_loc}\n***")
    fit_simulation(results_dir)



json_path = results_top_dir / 'summary.json'

with open(json_path, "w") as json_file:
    json.dump(fitting_summary_multi, json_file, indent=4)



