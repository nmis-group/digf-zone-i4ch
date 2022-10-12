
## Node-red (modbus-flow)
- Modbus read node (settings: FC- FC3:read holding registers, Unitid:1, Address:16 or 18, Quantity:62, poll rate:10ms, host:10.5.140.18)
- Firstout node (shows the data read from the modbus read node)
- buffer-parser node (add channels to output data after converting to data type:float, only 31 items were added since the offset is limited to 120)
- Format node (change data format ready to be written to a influxdb bucket/database)
- influxdb node (specify the server with URL:http://localhost:8086 and API token, orgnisation:NMIS, bucket:radial_forge_v2, measurment: forge_data_v1)

![modbus_flow](/images/modbus_flow_node_red.png)
- files can be imported and exported as .json (when importing it should be imported as a new flow)

![modbus_flow](../images/modbus_flow_node_red.png)


## Access influxdb database and query data
- influxdb bucket is stored at 
    ```/var/lib/influxdb/engine/data```
- Install the InfluxDB Python library:
    ```pip install influxdb-client```
- Instantiate the client
    ```import influxdb_client                   ```
       
    ```bucket = "<my-bucket>"                   ```
    ```org = "<my-org>"                         ```
    ```token = "<my-token>"                     ```

    ```  url="http://localhost:8086"            ```

    ``` client = influxdb_client.InfluxDBClient(```
    ``` url=url,                                ```
    ``` token=token,                            ```
    ```org=org                                  ```
    ```)                                        ```
- Instantiate the query client
    ```query_api = client.query_api()```
- Create a Flux query
- Pass the query method to create results or a dataframe (install pandas library if creating a dataframe) using the query client

## Influxdb write data into pd dataframes
- Create a pd dataframe
``` df = client.query_api().query_data_frame(org=my_org, query=query)```
- DataFrame must have the timestamp column as an index for the client
- Intialise the dataframe
```write_api = client.write_api(write_options=SYNCHRONOUS)```
- Write data to influxdb specified bucket with user defined measurement names
```write_api.write(bucket=bucket, org=org, record=tabel_name, data_frame_measurement_name='measurement_name',
                    data_frame_tag_columns=['column name])```
