# Data Engineering with Snowpark and visualization with Streamlit

## Context
**INEGI** is an autonomous public agency responsible for regulating and coordinating the National System of Statistical and Geographic Information, as well as for gathering and disseminating information on Mexico's territory, resources, population and economy, which makes it possible to provide information on the country's characteristics and aid in decision-making. It publishes the [get information by queries](https://www.inegi.org.mx/siscon/) from which public data sets can be taken.

### Complication
- The Institute generates basic statistics, which it obtains from three types of sources: censuses, surveys and administrative records, as well as derived statistics, through which it produces demographic, social and economic indicators, in addition to national accounting. This data is a widely used source for analysis in all types of industries, however it can have interesting challenges such as access as it is stored in file formats, the data can require processing to be used for example it is not formatted correctly for science or data visualization as well as some data quality issues such as containing null (NULL) data (*) in some columns.

### Your mission / What will you develop? 
- In this guide you will learn how to build a web application using Streamlit, an open source application development framework in Python language, will perform a data engineering process load, data type transformation (latitude/longitude) in Python in Snowflake Data Cloud.
![App](https://github.com/HeysolRacing/snowpark_inegi-main)

### Requirements 
- Access to [GitHub](https://github.com/)  
- [VSCode](https://code.visualstudio.com/download) with Jupyter Notebook
- [SnowSQL](https://developers.snowflake.com/snowsql/)  
- [Python](https://www.python.org/) (Python 3.8)
- [Anaconda](https://www.anaconda.com/products/distribution)
- Snowpark Python 
- Streamlit 

### Architecture Diagram
![Architecture and service model from file download in source data provider hosting, data extraction and transformation with Snowpark Python, data loading using code to an internal stage with Snowflake, with a Streamlit interface using Python to implement data visualization.](https://github.com/HeysolRacing/snowpark_inegi-main/blob/master/img/modelo.png)


## Setup
<h4>Code</h4>
Download the repository that contains the code at [Github repo](https://github.com/HeysolRacing/snowpark_inegi-main.git):

```shell
git clone https://github.com/HeysolRacing/snowpark_inegi-main.git
```
After downloading the project, go to the **snowpark_inegi-main** folder and open it with Visual Studio Code or your preferred editor that supports Jupyter Notebook files.

<h4>Creation of Python development environment</h4>. 
Create a local development environment for the installation of some libraries as well as Snowpark with Python 3.8 version.
Having Anaconda installed with the terminal or command line application, inside the folder where I download the github repository(clone), to create a development environment run:

```shell
conda create --name snowpark_env python=3.8 
conda activate snowpark_env
```

<h4>Snowpark Python Installation</h4>. 
Snowpark Installation

```shell
pip install snowflake-snowpark-python pandas
pip install lat-lon-parser
pip install requests
pip install notebook
conda install -c conda-forge streamlit 
conda install -c conda-forge pillow
```

### Set up config.py
In the Snowflake URL https://<account_id>.<account_region_zone>.snowflakecomputing.com example: https://ly14496.south-central-us.azure.snowflakecomputing.com the corresponding values are:

account_id = ly14496<br>
account_region_zone = south-central-us.azure<br>

In this config.py file enter the values for each property with the information to access Snowflake from Python using Snowpark.

```python
connection_parameters = {
    "account": "account_id.account_region_zone",
    "user": "user_snowflake",
    "password": "password_snowflake",
    "warehouse": "INEGI_WH",
    "role": "INEGI_ROLE",
    "database": "INEGI",
    "schema": "PUBLIC"
}
```

### In the environment <b>Snowflake UI(Web)</b> execute everything with <b>ACCOUNTADMIN</b> role:

```sql
use role accountadmin;
--objects 
create database inegi;
--warehouse
create warehouse inegi_wh 
warehouse_type = 'STANDARD' 
warehouse_size =XSMALL 
auto_suspend = 120 
auto_resume = TRUE 
max_cluster_count=1 
min_cluster_count=1;
--role
create role inegi_role;
grant role inegi_role to user <snowflake_user>;
grant role sysadmin to user <snowflake_user>;
grant role sysadmin to role inegi_role;
--privileges  
grant usage on database inegi to role inegi_role;
grant all privileges on schema public to role inegi_role;
grant usage on warehouse inegi_wh to role inegi_role;
```

## Execute

### Notebook and development environment (terminal or VSC) activation:
```shell
jupyter notebook
conda activate snowpark_env
```

Run in Jupyter Notebook for each of the following Notebooks, you can do it in Visual Studio Code (or terminal) run:

<ul>
<li><b>01_INEGI_download.ipynb</b></li>
Execute the cell which will perform the process of extracting, transforming and partitioning the CSV source to JSON.

```python
#Script for file download execution and transformations (Split to JSON)
from inegidata import urlDownload
# opción 'remote' for download from INEGI's webhost
# opciób 'local' for decompression from local repo
urlDownload('remote')
```

<li><b>02_INEGI_dataEngineering.ipynb</b></li>
<ol>
<li>Execute the first two cells to load the necessary libraries and activate the Snowflake session.</li>
<li>Execute the cell #Activation to create Snowflake objects and privileges</li>
<li>Execute the cell #Create internal Stage for loading already curated JSON data</li>
<li>Execute the cell #Transforming to Snowflake object for placing data into Snowflake table object</li>
</ol>

<li><b>03_INEGI_dataModeling.ipynb</b></li>
<ol>
<li>Execute the first two cells to load the necessary libraries and activate the Snowflake session.</li>
<li>Execute the cell #Create view to create the view that will have the data including JSON data transformation in INEGI_RAW table.</li>
<li>Execute the cell #UDF statement to incorporate the function created in python nom_entity that will be used to convert entity No. to entity name.</li>
<li>Execute the cell #View with totals by entity applying to materialize data applying UDF and which will have the maximum population totals for each 
    entity.</li>
<li>Execute the cell #Validate view only with totals per entity to validate the content of the created view.</li>
</ol>

<li><b>04_Streamlit.py</b><br>
 
To run the web application you can use Visual Studio Code (or another terminal)::
 
 ```shell
streamlit run Homepage.py
```

</li>
</ul>