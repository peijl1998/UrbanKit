# UrbanKit Deployment Tutorial



- Clone this repo

  ```shell
  git clone https://github.com/peijl1998/UrbanKit.git
  ```

- For urban_kit_frontend (root_path = "xxx/urban_kit_frontend")

  - Get your BaiduMap token(**AK**) from https://lbsyun.baidu.com/apiconsole/key#/home

  - Fill the **AK** in the `index.html ` and `src/main.js`  (indicated by ak:xxxx)

  - install nodejs dependencies

    ```shell
    npm install
    ```

  - start the frontend

    ```shell
    npm run start
    ```

- For urban_kit_backend (root_path = "xxx/urban_kit_backend")

  - install mongodb

    ```shell
    apt install mongodb
    ```

  - install required python libs

    ```shell
    pip install django
    pip install django-cors-headers
    pip install pymongo
    pip install geopy
    pip install torch torchvision fastdtw lightgbm
    ```

  - some operations on mongodb

    ```shell
    # interactive mongodb
    mongo
    
    > use urbankit
    > db.createUser({user:"root",pwd:"123456",roles:[{role:"dbAdmin",db:"urbankit"}]})
    ```

  - some preparations

    ```shell
    mkdir Config
    echo "{}" > ./Config/SI-AGAN.cfg
    ```

  - start backend

    ```shell
    python3 manage.py runserver 0.0.0.0:8000
    ```

- Start the service

  - assign the backend addr in `src/api/global_config.js` (like addr in "start backend" command)

  - create `user_config.json` in the root path of repo (the path of user_config_example.json), fill in your mongodb config, like 

    ```json
    {
            "mongodb": {
                    "database": "urbankit",
                    "user": "root",
                    "password": "123456",
                    "address": "127.0.0.1",
                    "port": "27017"
            }
    }
    ```

  - upload the demo.csv and enjoy it:)
  
    - NOTE: set attribute in the MapController at first.
    - for interpolation model, you can upload the demo model in the UrbanModels/Generator.pth



