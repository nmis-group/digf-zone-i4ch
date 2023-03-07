# Import required packages
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import holoviews as hv
import hvplot.pandas
import panel as pn
import data_processing_methods as dpm
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import DotProduct, WhiteKernel
import datetime as dt
from panel.template import DarkTheme
import datetime
import plot_functions as pf


# Read the dataframe with burner settings
burner_settings_df = pd.read_excel('Burners_settings_vs_O2 _rev1.xlsx', sheet_name='Sheet1')

# Standardise the model inputs and model outputs
standardised_1_df = burner_settings_df.copy()
for col in burner_settings_df.columns:

    if (np.std(burner_settings_df[col])> 0):
        standardised_1_df[col] = dpm.standardise(burner_settings_df[col],np.mean(burner_settings_df[col]),np.std(burner_settings_df[col]))
    else:
        standardised_1_df = standardised_1_df.drop(columns=col)

X1 = standardised_1_df.drop(columns =['Output O2 / %', 'Output Burner usage / %'])
y1 = standardised_1_df['Output O2 / %']
y2 = standardised_1_df['Output Burner usage / %']

# Drop columns with corr coeffcients higher than 0.9 
X1 = X1.drop(columns =['Burner turns from zero', 'Fan speed / RPM',' damper range / % (low)','damper range / % (High)'])
X1_train = X1[10:]
y1_train = y1[10:]
y2_train = y2[10:]

# Train Gaussian Process regression model
kernel = DotProduct() + WhiteKernel()
gpr_2 = GaussianProcessRegressor(kernel=kernel,
         random_state=0).fit(X1_train, y2_train)

gpr_1 = GaussianProcessRegressor().fit(X1_train, y1_train)

y1_std = np.std(burner_settings_df['Output O2 / %'])
y1_mean = np.mean(burner_settings_df['Output O2 / %'])

y2_std = np.std(burner_settings_df['Output Burner usage / %'])
y2_mean = np.mean(burner_settings_df['Output Burner usage / %'])


def plot_predictions():
    
    """
    Description
    -----------
        The plot functions for predicting O2 output and burner usage
    
    """
    
    # Predictions for O2 output with upper and lower bound
    X1_predict = X1
    y_gpr_mean, y_gpr_std = gpr_1.predict(X1_predict, return_std=True)
    y1_actual = y1
    Y1_df = pd.DataFrame(y_gpr_mean*y1_std+y1_mean, columns=['Predicted O2'])
    Y1_df['Actual O2'] = y1_actual*y1_std+y1_mean
    Y2_df = Y1_df.copy()
    RMS_1 = np.sqrt(np.mean(np.square(Y2_df['Actual O2']-Y2_df['Predicted O2'])))
    
    Y2_df['Upper bound'] = (y_gpr_mean-3*y_gpr_std)*y1_std+y1_mean
    Y2_df['Lower bound'] = (y_gpr_mean+3*y_gpr_std)*y1_std+y1_mean
    
    fig_a = Y2_df.hvplot(xlabel = 'Set point', height=500, width=1200, grid= True, 
                         color=["#d83569","#ec6608", '#6f7271', '#6f7271'])
    fig_area = Y2_df.hvplot.area(x='index', y='Lower bound', 
                                 y2='Upper bound').opts(color = '#6f7271',fill_alpha=0.5,height=250, width=1200,ylim =(-10,120), show_grid= True)
    fig_O2_output = fig_a*fig_area*hv.Text(5, 10, 'RMS error - O2 output = 0.53').opts(color='white')
    
    # Predictions for burner usage with upper and lower bound
    X2_predict = X1
    y2_gpr_mean, y2_gpr_std = gpr_2.predict(X2_predict, return_std=True)
    y2_actual = y2
    Y3_df = pd.DataFrame(y2_gpr_mean*y2_std+y2_mean, columns=['Predicted burner usage'])
    Y3_df['Actual burner usage'] = y2_actual*y2_std+y2_mean
    Y4_df = Y3_df.copy()
    RMS_2 = np.sqrt(np.mean(np.square(Y4_df['Actual burner usage']-Y4_df['Predicted burner usage'])))
    
    Y4_df['Upper bound'] = (y2_gpr_mean-3*y2_gpr_std)*y2_std+y2_mean
    Y4_df['Lower bound'] = (y2_gpr_mean+3*y2_gpr_std)*y2_std+y2_mean
    
    fig_a2 = Y4_df.hvplot(xlabel = 'Set point', height=500, width=1200,ylim =(-10,120),grid= True, 
                         color=["#368dbc", "#8ec79a", '#6f7271', '#6f7271'])
    fig_area2 = Y4_df.hvplot.area(x='index', y='Lower bound', y2='Upper bound').opts(color = '#6f7271',
                                fill_alpha=0.5,height=250, width=1200,  ylim =(0,120),show_grid= True)
    fig_burner_usage = fig_a2*fig_area2*hv.Text(5, 80, 'RMS error - burner usage = 4.52').opts(color='white')
    
    return fig_burner_usage*fig_O2_output


def plot_predictions_b(text_box_1,text_box_2,text_box_3,text_box_4):
        
    """
    Description
    -----------
        The plot functions for predicting O2 output given the 
        new burner settings given by the user
    
    """

    X_cols = list(X1_train.columns)
    X_new = pd.DataFrame([[int(text_box_1),int(text_box_2),int(text_box_3),int(text_box_4)]],
                         columns = X_cols)
    X_new.reset_index(drop=True, inplace=True)
    X_new_pr= X_new.copy()
    for col in X_cols:    
        X_new_pr[col] = dpm.standardise(X_new[col],np.mean(burner_settings_df[col]),np.std(burner_settings_df[col]))

    y_new_predict = gpr_1.predict(X_new_pr)
    Y_new = pd.DataFrame(y_new_predict*y1_std+y1_mean, columns=['Newly Predicted'])

    num1 = pn.indicators.Number(name='O2 Predictions', value=float(y_new_predict*y1_std+y1_mean), font_size ='35pt', format='{value:.2f}%', default_color ='white')
    y2_new_predict = gpr_2.predict(X_new_pr)
    Y2_new = pd.DataFrame(y2_new_predict*y2_std+y2_mean, columns=['Newly Predicted'])

    num2 = pn.indicators.Number(name='Burner usage', value=float(y2_new_predict*y2_std+y2_mean), font_size ='35pt', format='{value:.2f}%', default_color ='white')
    num = pn.Column(num1,num2)
    return num


# No. samples to be generated
N_samples = 5000
cols = list(X1_train.columns)

# Initialise arrays to store samples of un-standardised and 
# standardised inputs
D = len (cols)
X_samples_us = np.zeros([N_samples, D])
X_samples = np.zeros([N_samples, D])

for i in range(N_samples):
    for j in range (D):
        X_samples_us[i, j] = np.random.uniform(np.min(burner_settings_df[cols[j]]), np.max(burner_settings_df[cols[j]]))

# Standardise the samples created
for j in range (D):    
    X_samples[:,j] = dpm.standardise(X_samples_us[:,j],np.mean(burner_settings_df[cols[j]]),np.std(burner_settings_df[cols[j]]))

# Save the predictions 
X_samples_df = pd.DataFrame(data = X_samples, columns = cols)
X_samples_us_df = pd.DataFrame(data = X_samples_us, columns = cols)
y_samples_predict = gpr_1.predict(X_samples_df)
y_samples_predict = y_samples_predict*y1_std+y1_mean
X_samples_us_df['Predicted O2 %'] = y_samples_predict

def samples_cols():
    cols_samples = list(X_samples_us_df.columns)
    return cols_samples

cols = samples_cols()
y_samples = pn.widgets.Select(name='Chose a signal', options=cols, value='Temperature setpoint / degC')
    
@pn.depends(y_samples.param.value)
def plot_main_effects(y_samples,slider_pos_temp,slider_pos_O2):
            
    """
    Description
    -----------
        The plot functions for generating scatter plots 
        for random burner setting samples
    
    """
    # Find the mean of each bin (binning data)
    n_bins = 30
    x_plot = X_samples_us_df[y_samples]
    y_plot = X_samples_us_df['Predicted O2 %']

    bins = np.linspace(np.min(x_plot), np.max(x_plot), n_bins)
    main_effect = np.zeros(len(bins)-1)
    main_effect_index = np.zeros(len(bins)-1)
    main_effect_df = pd.DataFrame({})

    
    for j in range(len(bins)-1):
        indx = np.logical_and(x_plot > bins[j], x_plot < bins[j+1])
        main_effect_index[j] = 0.5*(bins[j] + bins[j+1])

        # Only compute mean if there are any points in bin
        if np.sum(indx) > 0:
            main_effect[j] = np.mean(y_plot[indx])

    main_effect_df['index'] = main_effect_index
    main_effect_df['value'] = main_effect
    
    # plot horizontal and vertical lines for x-y limits  
    if (y_samples == 'Temperature setpoint / degC'):
        vline1 = hv.VLine(int(slider_pos_temp))
        vline1.opts(color= '#d83569')
        
        h1line = hv.HLine(int(slider_pos_O2))
        h1line.opts(color= '#d83569')

                
    # plot main effects of model inputs
    fig_c = X_samples_us_df.hvplot.scatter(x = y_samples, y = 'Predicted O2 %', height = 500, width = 1100, ylim =(-5,15), 
                                           hover_cols = 'all', color="#368dbc", grid = True )

    if (y_samples == 'Temperature setpoint / degC'):
        fig = fig_c*vline1*h1line
    
        ind1 = np.logical_and(X_samples_us_df['Temperature setpoint / degC']>(slider_pos_temp-0.1),
                              X_samples_us_df['Temperature setpoint / degC']<(slider_pos_temp+0.1))
        X_samples_a_df = X_samples_us_df[ind1]
        ind2 = np.logical_and(X_samples_a_df['Predicted O2 %']<(slider_pos_O2+0.1),
                              X_samples_a_df['Predicted O2 %']>(slider_pos_O2-0.1))
        sorted_df = X_samples_a_df[ind2].sort_values(by=['Predicted O2 %'],ignore_index = True)

        if len(sorted_df)>0:
            num1 = pn.indicators.Number(name='Fan setpoint', value=np.round(sorted_df['Fan setpoint / %'][0]), format='{value}%',font_size ='35pt', default_color ='white')
            num2 = pn.indicators.Number(name='Burner apporx. value', value=np.round(sorted_df['Burner approx value'][0]), format='{value}',font_size ='35pt', default_color ='white')
            num3 = pn.indicators.Number(name='Red valve', value=np.round(sorted_df['Red valve'][0]),font_size ='35pt', format='{value}', default_color ='white')
            num = pn.Column(num1,num2,num3)
            fig_out = pn.Row(num,fig)
        else: fig_out = fig 
    else:
        fig_out = fig_c
    return fig_out

pn.config.throttled = True
df_merged = pd.read_pickle('merged_sensor_df.pkl')
df_merged = df_merged.resample('1T').mean()

def roof_columns():
    cols_1 = list(df_merged.columns[df_merged.columns.str.startswith('ROOF_0104_300_')])
    return cols_1
temp_columns = roof_columns()
se_roof = pn.widgets.Select(name='Chose a signal to tune filtering parameters', options=temp_columns ,value='ROOF_0104_300_10_TC')

@pn.depends(se_roof.param.value)
def plot_trunc_furnace_data(date_start, date_end, se_roof,slider_pos,Remove_spikes = False):
            
    """
    Description
    -----------
        The plot functions for visulaising roof temperature
        sensor data
    
    """
    df_merged_truncated = df_merged.loc[:,df_merged.columns.str.startswith('ROOF_0104_300_')]
    df_merged_truncated = df_merged_truncated [date_start: date_end]
    df_merged_filtered = df_merged_truncated.copy()
    if Remove_spikes:
        df_merged_filtered.loc[:,se_roof] = dpm.remove_spikes(df_merged_truncated.loc[:,se_roof],olr_def=1)
    
    df_merged_filtered.loc[:,se_roof] = dpm.low_pass_filter(df_merged_filtered.loc[:,se_roof],wn=slider_pos)
    temp_lines = {i: hv.Curve((df_merged_truncated[i])) for i in temp_columns}
    fig_e = hv.NdOverlay(temp_lines, kdims='signals').opts(height = 400, width=1400, show_grid = True,legend_position = 'right', ylabel ='Roof temperature readings')
    fig_f = df_merged_filtered.hvplot.line(y = se_roof, height = 400, width = 1400, color= 'white', label = 'Filtered signal',line_width = 2, ylim =(0,1200))
    return fig_e*fig_f


def PID_columns():
    cols_2 = list(df_merged.columns[df_merged.columns.str.startswith('PID_ZONE_1')])
    return cols_2
PID_col = PID_columns()
se_PID = pn.widgets.Select(name='Chose a signal to tune filter parameters', options=PID_col ,value='PID_ZONE_1_PV')

@pn.depends(se_PID.param.value)
def plot_trunc_PID_data(date_start, date_end, se_PID,slider_pos,Remove_spikes = False):
                
    """
    Description
    -----------
        The plot functions for visulaising PID zone 1
        sensor data
    
    """
    df_PID_truncated = df_merged.loc[:,df_merged.columns.str.startswith('PID_ZONE_1')]
    df_PID_truncated = df_PID_truncated [date_start: date_end]
    df_PID_filtered = df_PID_truncated.copy()
    
    if Remove_spikes:
        df_PID_filtered.loc[:,se_PID] = dpm.remove_spikes(df_PID_truncated.loc[:,se_PID],olr_def=1)
    
    df_PID_filtered.loc[:,se_PID] = dpm.low_pass_filter(df_PID_filtered.loc[:,se_PID],wn=slider_pos)
    
    PID_lines = {i: hv.Curve((df_PID_truncated[i])) for i in PID_col}
    fig_g = hv.NdOverlay(PID_lines, kdims='signals').opts(height = 400, width=1400, show_grid = True,legend_position = 'right', ylabel ='PID zone sensor readings')
    fig_h = df_PID_filtered.hvplot.line(y = se_PID, height = 400, width = 1400, color= 'white', label = 'Filtered signal',line_width = 2, ylim =(0,1200))
    
    return fig_g*fig_h

def Gas_columns():
    cols_gas = list(df_merged.columns[df_merged.columns.str.startswith('GAS_')])
    return cols_gas

cols_gas = Gas_columns()
y_gas = pn.widgets.Select(name='Chose a signal to tune filtering parameters', options=cols_gas ,value='GAS_0110_943_14_PT')
df_gas_merged_selected = df_merged.loc[:,df_merged.columns.str.startswith('GAS_')][dt.datetime(2022, 9, 27): dt.datetime(2022, 10, 14)]

@pn.depends(y_gas.param.value)
def plot_gas_data(slider_pos, y_gas, Remove_spikes = False):
                
    """
    Description
    -----------
        The plot functions for processing gas flow signals
    
    """
    
    df_gas_merged_filtered = df_gas_merged_selected.copy()
    
    if Remove_spikes:
        df_gas_merged_filtered.loc[:,y_gas] = dpm.remove_spikes(df_gas_merged_selected.loc[:,y_gas],olr_def=1)    
    df_gas_merged_filtered.loc[:,y_gas] = dpm.low_pass_filter(df_gas_merged_filtered.loc[:,y_gas],wn=slider_pos)
    
    # Standardise input data
    df_gas_std_filtered_df = df_gas_merged_filtered.copy()
    df_gas_std_selected_df = df_gas_merged_selected.copy()
    for col in cols_gas:

        if (np.std(df_gas_merged_filtered[col])> 0):
            df_gas_std_filtered_df[col] = dpm.standardise(df_gas_merged_filtered[col],np.mean(df_gas_merged_filtered[col]),np.std(df_gas_merged_filtered[col]))
            df_gas_std_selected_df[col] = dpm.standardise(df_gas_merged_selected[col],np.mean(df_gas_merged_selected[col]),np.std(df_gas_merged_selected[col]))
        else:
            df_gas_std_filtered_df = df_gas_std_filtered_df.drop(columns=col)
            df_gas_std_selected_df = df_gas_std_selected_df.drop(columns=col)    
    
    gas_cols = df_gas_std_selected_df.columns
    gas_lines = {i: hv.Curve((df_gas_std_selected_df[i])) for i in cols_gas}
    fig_m = hv.NdOverlay(gas_lines, kdims='signals').opts(height = 400, width=1400, show_grid = True,legend_position = 'right', ylabel ='Gas flow sensor readings')
    fig_gas_line = df_gas_std_filtered_df.hvplot.line(y = y_gas, height = 400, width = 1300, color= 'white', label = 'Filtered signal',line_width = 2)
    return fig_m*fig_gas_line

def Air_columns():
    cols_air = list(df_merged.columns[df_merged.columns.str.startswith('AIR_')])
    return cols_air

cols_air = Air_columns()
y_air = pn.widgets.Select(name='Chose a signal to tune filtering parameters', options=cols_air ,value='AIR_0123_945_03_PT')
df_air_merged_selected = df_merged.loc[:,df_merged.columns.str.startswith('AIR_')][dt.datetime(2022, 9, 27): dt.datetime(2022, 10, 14)]

@pn.depends(y_air.param.value)
def plot_air_data(slider_pos, y_air, Remove_spikes = False):
                    
    """
    Description
    -----------
        The plot functions for processing air flow signals
    
    """    
    df_air_merged_filtered = df_air_merged_selected.copy()
    
    if Remove_spikes:
        df_air_merged_filtered.loc[:,y_air] = dpm.remove_spikes(df_air_merged_selected.loc[:,y_air],olr_def=1)
    
    df_air_merged_filtered.loc[:,y_air] = dpm.low_pass_filter(df_air_merged_filtered.loc[:,y_air],wn=slider_pos)
    
    
    # Standardise input data
    air_std_filtered_df = df_air_merged_filtered.copy()
    air_std_selected_df = df_air_merged_selected.copy()
    for col in cols_air:

        if (np.std(df_air_merged_filtered[col])> 0):
            air_std_filtered_df[col] = dpm.standardise(df_air_merged_filtered[col],np.mean(df_air_merged_filtered[col]),np.std(df_air_merged_filtered[col]))
            air_std_selected_df[col] = dpm.standardise(df_air_merged_selected[col],np.mean(df_air_merged_selected[col]),np.std(df_air_merged_selected[col]))
        else:
            air_std_filtered_df = air_std_filtered_df.drop(columns=col)
            air_std_selected_df = air_std_selected_df.drop(columns=col)   
    
    air_cols = air_std_selected_df.columns
    air_lines = {i: hv.Curve((air_std_selected_df[i])) for i in air_cols}
    fig_k = hv.NdOverlay(air_lines, kdims='signals').opts(height = 400, width=1400, show_grid = True,legend_position = 'right', ylabel ='Air flow sensor readings')
    fig_air_line = air_std_filtered_df.hvplot.line(y = y_air, height = 400, width = 1300, color= 'white', label = 'Filtered signal',line_width = 2)
    
    return fig_k*fig_air_line

O2_truncated = df_merged.loc[:,df_merged.columns.str.startswith('FURNACE_0126_341_04_O2')][dt.datetime(2022, 9, 27): dt.datetime(2022, 10, 14)]

# Define function for ploting  O2 sensor data
def plot_O2_data(slider_pos, Remove_spikes = False):
                    
    """
    Description
    -----------
        The plot functions for processing O2 output
    
    """
    O2_filtered = O2_truncated.copy()
    
    if Remove_spikes:
        O2_filtered.loc[:,'FURNACE_0126_341_04_O2'] = dpm.remove_spikes(O2_truncated.loc[:,'FURNACE_0126_341_04_O2'],olr_def=1)
    
    O2_filtered.loc[:,'FURNACE_0126_341_04_O2'] = dpm.low_pass_filter(O2_filtered.loc[:,'FURNACE_0126_341_04_O2'],wn=slider_pos)
    
    df_std_O2_truncated = O2_truncated.copy()
    df_std_O2_filtered = O2_filtered.copy()
    df_std_O2_truncated.loc[:,'FURNACE_0126_341_04_O2'] = dpm.standardise(O2_truncated.loc[:,'FURNACE_0126_341_04_O2'],
                                                                             np.mean(O2_truncated.loc[:,'FURNACE_0126_341_04_O2']),
                                                                             np.std(O2_truncated.loc[:,'FURNACE_0126_341_04_O2']))
    df_std_O2_filtered.loc[:,'FURNACE_0126_341_04_O2'] = dpm.standardise(O2_filtered.loc[:,'FURNACE_0126_341_04_O2'],
                                                                             np.mean(O2_filtered.loc[:,'FURNACE_0126_341_04_O2']),
                                                                             np.std(O2_filtered.loc[:,'FURNACE_0126_341_04_O2']))
    
    O2_cols = df_std_O2_truncated.columns
    O2_lines = {i: hv.Curve((df_std_O2_truncated[i])) for i in O2_cols}
    fig_i = hv.NdOverlay(O2_lines, kdims='signals').opts(height = 400, width=1400, show_grid = True,legend_position = 'right', ylabel ='O2 flow sensor readings')
    fig_j = df_std_O2_filtered.hvplot.line(y = 'FURNACE_0126_341_04_O2', height = 400, width = 1100, color= 'white', label = 'Filtered signal',line_width = 2)
    
    return fig_i*fig_j

# REad air flow sensor data
df_air_train_selected = df_merged.loc[:, df_merged.columns.str.startswith('AIR_')]
df_air_train_filtered = df_air_train_selected.copy()

for col in cols_air:
    df_air_train_filtered.loc[:,col] = dpm.remove_spikes(df_air_train_selected.loc[:,col],olr_def=1)
    df_air_train_filtered.loc[:,col] = dpm.low_pass_filter(df_air_train_filtered.loc[:,col],wn=0.1)
    
# Read gas flow sensor data    
df_gas_train_selected = df_merged.loc[:, df_merged.columns.str.startswith('GAS_')]
df_gas_train_filtered = df_gas_train_selected.copy()

for col in cols_gas:
    df_gas_train_filtered.loc[:,col] = dpm.remove_spikes(df_gas_train_selected.loc[:,col],olr_def=1)
    df_gas_train_filtered.loc[:,col] = dpm.low_pass_filter(df_gas_train_filtered.loc[:,col],wn=0.1)

# Read O2 sensor data    
cols = list(df_merged.columns[df_merged.columns.str.startswith('FURNACE_0126_341_04_O2')])

df_O2_selected = df_merged.loc[:, df_merged.columns.str.startswith('FURNACE_0126_341_04_O2')]
df_O2_filtered = df_O2_selected.copy()

for col in cols:
    df_O2_filtered.loc[:,col] = dpm.remove_spikes(df_O2_selected.loc[:,col],olr_def=1)
    df_O2_filtered.loc[:,col] = dpm.low_pass_filter(df_O2_filtered.loc[:,col],wn=0.01)

df_flow_combined = pd.concat([df_air_train_filtered, df_gas_train_filtered], axis=1)
df_flow_combined = pd.concat([df_flow_combined,df_O2_filtered], axis=1)
df_flow_combined = df_flow_combined[30000:-100]

# Standardise input data
standardised_df = df_flow_combined.copy()
for col in df_flow_combined.columns:

    if (np.std(df_flow_combined[col])> 0):
        standardised_df[col] = dpm.standardise(df_flow_combined[col],np.mean(df_flow_combined[col]),np.std(df_flow_combined[col]))
    else:
        standardised_df = standardised_df.drop(columns=col)

y = standardised_df['FURNACE_0126_341_04_O2']
X = standardised_df

# Drop columns with corr coeffcients higher than 0.9 
X = X.drop(columns =['AIR_DRIVE_AIR_SPEED', 'AIR_0123_945_03_PT', 'GAS_0110_943_14_PT', 'GAS_0110_943_07_FT_m3_h'])

tdate = datetime.datetime(2022, 10, 1)
ldate = datetime.datetime(2022, 10, 5)
vdate = datetime.datetime(2022, 10, 8)
def plot_standardised_data():
                    
    """
    Description
    -----------
        The plot functions for visualising processed air,gas and O2
    
    """
    x_cols = X.columns
    lines = {i: hv.Curve((X[i])) for i in x_cols}
    fig_n = hv.NdOverlay(lines, kdims='signals').opts(height = 400, width=1400, show_grid = True,legend_position = 'right', ylabel ='Sensor readings')
    
    vline_date = hv.VLine(ldate).opts(color= '#3e4765',line_dash='dashed')
    
    return fig_n* vline_date*hv.Text(tdate, 5, 'Training period').opts(color='white')*hv.Text(vdate, 5, 'Validation period').opts(color='white')

# Select the datafor training
X_train = X[0:int(len(X)/2)]
y_train = y[0:int(len(X)/2)]

# Train Gaussian Process regression model
gpr = GaussianProcessRegressor().fit(X_train, y_train)
y_std = np.std(df_flow_combined['FURNACE_0126_341_04_O2'])
y_mean = np.mean(df_flow_combined['FURNACE_0126_341_04_O2'])

# Make predictions with model trained using gas and air flows
X_predict = X
y_predict_mean,y_predict_std = gpr.predict(X_predict, return_std=True)
y = y.reset_index()

# Save results
y_actual = y['FURNACE_0126_341_04_O2']
Y_df = pd.DataFrame(y_predict_mean*y_std+y_mean, columns=['Predicted'])
Y_df['Actual'] = y_actual*y_std+y_mean
Y_df['Upper bound (1 std)'] = (y_predict_mean+1*y_predict_std)*y_std+y_mean
Y_df['Lower bound (1 std)'] = (y_predict_mean-1*y_predict_std)*y_std+y_mean
Y_df['Upper bound (3 std)'] = (y_predict_mean+3*y_predict_std)*y_std+y_mean
Y_df['Lower bound (3 std)'] = (y_predict_mean-3*y_predict_std)*y_std+y_mean
Y_df['Date'] = y['Date']
Y_df.set_index('Date',inplace=True)

#summary statistics
RMS = np.sqrt(np.mean(np.square(Y_df['Actual']-Y_df['Predicted'])))
countifs_3std = sum((Y_df.Actual >= (y_predict_mean-3*y_predict_std)*y_std+y_mean) & (Y_df.Actual <= (y_predict_mean+3*y_predict_std)*y_std+y_mean))/len(Y_df.Predicted)

Y_df = Y_df[int(len(X)/2):]

def plot_predicted_data():
                    
    """
    Description
    -----------
        The plot functions for predicting O2 output using air and gas flow
    
    """

    fig_o = Y_df.hvplot(xlabel = 'Date',ylabel = 'O2 output', height=400, width=1400, grid= True, color=["#368dbc", "#8ec79a", '#6f7271', '#6f7271', '#6f7271', '#6f7271'])
    fig_o_area = Y_df.hvplot.area(x='Date', y='Lower bound (1 std)', 
                                 y2='Upper bound (1 std)').opts(color = 'white',fill_alpha=0.5, height=400, width=1400, show_grid= True)
    fig_o_area = Y_df.hvplot.area(x='Date', y='Lower bound (3 std)', 
                                 y2='Upper bound (3 std)').opts(color = 'white',fill_alpha=0.8, height=400, width=1400, show_grid= True)
    return fig_o_area*fig_o*hv.Text(vdate, 27, 'Validation preiod').opts(color='white')* hv.Text(vdate, 22, 'Root mean squared (RMS) = 0.8585').opts(color='white')* hv.Text(vdate, 17, 'Points within 1 std. = 93.72%').opts(color='white')* hv.Text(vdate, 12, 'Points within 3 std. = 100%').opts(color='white')
