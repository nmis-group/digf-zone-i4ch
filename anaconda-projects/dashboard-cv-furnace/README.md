 # Calorific Value (CV) furnace data
 
 ## Objectives
 
 The aim of this project is to visualise sensor data and predict O2 output using burner settings and also using air and gas flow sensor data captured during operation of a  CV furnace. Given the temperature and expected O2 we have predicted the optimum burner settings to be used in the shop floor environment using the developed ML model.
 
The project benefits the manufacturing industry by improving safety, increasing efficiency, reducing costs, optimizing processes, promoting sustainability, and ensuring product quality. The use of the predictive model, Gaussian Process Regression, enhances decision-making capabilities, allowing manufacturers to make informed adjustments and improvements in their furnace operations.

**Benefits of the project in the manufacturing industry include:**

- Enhanced Safety: By predicting the O2 output and monitoring it throughout the operation of the calorific value furnace, potential safety risks can be identified in advance. This allows manufacturers to take necessary precautions and ensure safe operating conditions, minimizing the risk of accidents, fires, or other hazards.

- Improved Efficiency: The predictive model, Gaussian Process Regression (GPR), helps optimize the operating conditions of the furnace. By accurately predicting the O2 output, manufacturers can adjust variables such as fuel input, airflow, or temperature settings to maintain optimal combustion. This leads to improved energy efficiency, reduced fuel consumption, and cost savings for the manufacturing process.

- Cost Reduction: Efficient utilization of natural gas in the furnace results in cost savings for manufacturers. By accurately predicting the O2 output and suggesting optimal operating conditions, the project enables manufacturers to optimize their resource usage, minimize waste, and reduce operational expenses.

- Process Optimization: The use of GPR allows for uncertainty measurements in the predictions. This feature is valuable in exploring unknown territories or scenarios. Manufacturers can make informed decisions about process optimization based on the uncertainty measures provided by the model. It helps them identify areas where the model is confident in its predictions and areas where further experimentation or caution might be necessary.

- Sustainability: By optimizing the O2 output and operating conditions, the project promotes sustainable manufacturing practices. Complete combustion and efficient energy utilization reduce the emission of unburned fuel and harmful pollutants, contributing to environmental sustainability and compliance with environmental regulations.

- Quality Control: The predictive model and the ability to suggest optimal operating conditions assist in maintaining consistent product quality. By monitoring and adjusting the O2 output, manufacturers can ensure that the combustion process remains stable, resulting in reliable and uniform product characteristics
 
 ## Instructions 
 The dashboard can be accessed using the following instructions:
 
- Install anaconda project (https://anaconda-project.readthedocs.io/en/latest/install.html)
- Once installed navigate to the folder using command line interface (eg: cd ~/digf-zone-i4ch/anaconda-projects/dashborad-cv-furnace/)
- If you are running on a desktop,then in anconda-project.yaml file change the following dashboard code  
```
unix: panel serve 06-fast_dashboard.ipynb --allow-websocket-origin=130.159.142.133:9090
```
to this code:
 ```
unix: panel serve 06-fast_dashboard.ipynb 
 ```
 - or if you are running the code on a server change the IP address and port appropriately
 - Then run the following command in your command line interface
 ```
 anaconda-project run dashboard --show 
 ```
 - Follow the instruction showing in the cmd and open a new web browser using the given http address to access the Bokeh server
 
