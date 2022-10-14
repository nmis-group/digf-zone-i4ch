## Scottish Manufacturing - dataexplorer 4.0

The codes clean and visualise data collected form Data city website realted to Scottish manufacturing sector found at (https://products.thedatacity.com/v2/home/)

### Install instructions

- Create a conda virtual environment using env.yml which will contain all the required packages
(e.g :pandas, holoviews)
- activate the enviornment 
(for more info :https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file) 
- If using notebook, install ipykernel
```conda install -c anaconda ipykernel```
- Include the conda environment in jupyter Notebook
```python -m ipykernel install --user --name=firstEnv```
- Choose the created virtual envirnment from the drop down menu in notebook terminal

### SME definition

The UK definition of SME is generally a small or medium-sized enterprise with fewer than 250 employees. While the SME meaning defined by the EU is also business with fewer than 250 employees, and a turnover of less than €50 million

### SME data visualisation

 - Geo distribution of SME by turn over and employees
 - Plot distribution of companies count by sector (using SIC code)
