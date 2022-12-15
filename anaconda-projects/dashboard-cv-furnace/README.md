 # Calorific Value (CV) furnace data
 
- Install anaconda project
- Once installed navigate to the folder using command line interface (eg: cd ~/digf-zone-i4ch/anaconda-projects/dashborad-cv-furnace/)
- If you are running on a desktop,then in anconda-project.yaml file change the dashboard code  
```
unix: panel serve furnace_dashboard.ipynb --allow-websocket-origin=130.159.142.133:9090
```
 like the following code:
 ```
unix: panel serve furnace_dashboard.ipynb 
 ```
 - or if you are running the code on a server change the IP address and port appropriately
 - Then run the following command in your command line interface
 ```anaconda-project run dashboard --show 
 ```
 - Follow the instruction showing in the cmd and open a new web browser using the given http address to access the Bokeh server
 