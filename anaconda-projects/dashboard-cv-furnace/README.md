 # Calorific Value (CV) furnace data
 
 The aim of this project is to visualise sensor data and predict O2 output using burner settings and also using air and gas flow sensor data captured during operation of a  CV furnace. Given the temperature and expected O2 we have predicted the optimum burner settings to be used in the shop floor environment using the developed ML model.
 
 The dashboard can be accessed using the following instructions 
 
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
 
