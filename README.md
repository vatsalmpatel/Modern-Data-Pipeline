## Before starting the Project

- Make sure you have your free snowflake account created as well create a free account on dbt

## Create a Conda ENV

```sh
conda create -n dbt_env
conda activate dbt_env
conda install pip
pip install dbt-core dbt-snowflake
```

## Create roles and warehouse on snowflake

- Run the following commands on snowflake, so that we have a role and a warehouse to work with on snowflake.

    1. Create a warehouse (compute) that can be used to execute all the queries and transformations. In order to create a compute (warehouse), we need to use the `accountadmin role.

        ```sh
        use role accountadmin;
        create warehouse dbt_wh with warehouse_size='x-small';
        ```

    2. Create database that we are going to use to store all the tables and final transformations

        ```sh
        create database if not exists dbt_db;
        ```

    3. Create a role

        ```sh
        create role if not exists dbt_role;
        ```

    4. Grant the role that we just created to our user, in my case it is `VATSALMPATEL`, and we also need to grant usage of the data warehouse to our role

        ```sh
        grant role dbt_role to user VATSALMPATEL;
        grant usage on warehouse dbt_wh to role dbt_role;
        ```

    5. Grant permission to `dbt_role:

        ```sh
        grant all on database dbt_db to role dbt_role;
        ```

    6. Finally create a schema in our database `dbt_db` using the role that we just created:

        ```sh
        use role dbt_role;
        create schema if not exists dbt_db.dbt_schema;
        ```

## Initialize dbt project

- Now, in your favourite terminal (I am using vscode), initialize the dbt project using dbt init:

    ```sh
    dbt init
    ```

- After this, in the terminal itself, it will ask for a project name, enter a project name, I am using `datapipeline` as the project name.

- Next, it will ask for Which database would you like to use, and in my case, I have only `dbt-connector` (snowflake connector) installed, I will choose the number, in my case it is `1`

- After this, it will ask you for you snowflake account identifier, for this go to snowflake account, and look for the identifier. Look at this link, so as to know how to specify the exact account identifier format depending on the clpud provider and region [Link](https://docs.snowflake.com/en/user-guide/admin-account-identifier#non-vps-account-locator-formats-by-cloud-platform-and-region)

- Next, it will ask for the dev username, and here you will enter dev username which is the username on your snowflake account and in my case it is `vatsalmpatel`.

- Next, it will ask for password, enter your account password.

- After this, it will ask you to fill in the role and warehose name on snowflake, enter the names of them respectively to whatever names you have given to your role and warehouse. In my case they were `dbt_role` and `dbt_wh` respectively for the role and warehouse names.

- Next it will ask you for the database name and schema name, enter the database name and schema name that we just created, which will be `dbt_db` and `dbt_schema` respectively.

- After all these steps, you will see a `datapipeline` directory created for us, so that we can start writing transformations. You will need to `cd` into that folder to run all the dbt commands.

    ```
    cd datapipeline
    ```

- Run the dollowing command to see if everything is working as it should, and if you setup everything correctly, you should receive `All checks passed!`

    ```sh
    dbt debug
    ```

- This is what the entire process looks like on the terminal:

![dbt_init_command_image](https://github.com/vatsalmpatel/dbt_project/blob/master/images/dbt_init.png)

## DBT Transformations:

- Just like a main function in `C++` that is the starting point in a `C` code, `dbt_project.yml` is the starting file for a dbt project. All the necessary information about the different model and how we want to materialize them in snowflake are written here. In our case, we want the `staging` tables to materialize as views and all the `marts` logic to materialize as tables in snowflake.

- All the transformations happend through `models` in dbt. In order to write all your transformations, we need to put them in the models folder, under different models. In our case, we have two, `staging` to create all our staging tables and `marts` that hold logic for all you final tables that use our staging tables.

- To get more information about the all the models and the transformation logic, you need to look at `datapipeline/models` folder and take a look at various models that we have in there.

- I am using the already available sample data in snowflake, but you can use whatever dataset you want to perform transformations.

- We can even write `Generic Tests` in dbt, that check a particular column against a specific set of values, you can take a look at an example at `datapipeline/models/marts/generic_tests.yml`. We can even write in the form of sqql queries, which returns rows which fail that daat quality check. You can take a look at an example at `datapipeline/tests/fct_orders_date_valid.sql` and `datapipeline/tests/fct_orders_discount.sql`.

## Commands used to apply the transformations:

1. `dbt run`: Execute models and apply transformations to raw data.
2. `dbt test`: Run data tests to validate data quality.
3. `dbt build`: Run all transformations, tests, and seeding in one command.
4. `dbt deps`: Install dbt packages listed in packages.yml, which we have in our case.
5. `dbt run --select model_name`: Execute specified model_name and apply transformations to raw data.

## Snowflake tables, after running the `dbt build command`:

![snowflake_tables_and_views](https://github.com/vatsalmpatel/dbt_project/blob/master/images/snowflake_ss.png)

- **As you can see, all the tables and views have been created in snowflake, as a result of running the `dbt build` command. This means, all the transformations have been applied to our data, following the ELT (Extract, Load and Transform), process, where the E and the L process was already done for us, we just performed the T (Transformation) part of the ELT pipeline.**

## Fivetran Integration

- Additionally, this repo also contains a `deployment.yml` file, which is used to run the jobs on Frvetran on a daily schedule, showcasing use case of Fivetran not just as an integration tool, but also as a tool that can be used to schedule `dbt transformations`. To make this work, go to the `Transformations` tab on Fivetran, setup a dbt transformation, which will ask you to fill out git repo which has the dbt transformations, with the above mentioned `deployment.yml` which will be used by Fivetran to specify when to run the job and what models to run during the job. In my example, I have set  it up to run all the models, but it can be used to run individual models as well. Look at the `datapipeline/deployment.yml` file for more information.

## Teardown and Cleanup:

- After you are done, you need to cleanup everything on snowflake, so that wwe do not incur any additional costs:

```sh
use role accountadmin;

drop warehouse if exists dbt_wh;
drop database if exists dbt_db;
drop role if exists dbt_role;
```

## Future Steps and Improvements:

1. We can orchestrate the pipeline (the entire transformation logic) using tools such as `Airflow`, where we can create DAG, and these DAGS will run periodically, and perform transformation on the incoming data.
2. We can also use a tool such as `Prefect` to orchestrate these transformations on a timely fashion. Both `Airflow` and `Prefect` have built-in functionality to run the pipeline again in case of failures and notify teams in case of failures.
3. Use this data in further downstream tasks such as data visualization or creating machine learning models to either gain more insights from the data from these visualizations using tools such as PowerBI or Google Looker, which can both connect to snowflake using connectors, or use this data clean it further and train some machine learning models such as Product Recommendations.

## Prefect Modification:

To use Prefect, first created a file `prefect_flow.py` with all the necessary `flows` and `tasks`. This file contains code to run the `dbt run` and `dbt test` commands that will materialize the necessary views and tables on Snowflake.

Now, to deploy the code and schedule it to run on a daily basis, we need to create what Prefect calls `deployment`. Now, there are multiple different ways to create deployment (serve, YAML deployment, deploy), we use the YAML deployment method. The step is very simple, we use the in-built recipe, that will use the code locally, and schedule the code on the local Prefect Server (can also be configureed to run using the Prefect Cloud backend). Here are the steps that you need to follow:

1. Start the Prefect Server:

    ```bash
    prefect server start
    ```

2. Make sure you have the Prefect code, in our case it is the `prefect_flow.py` file.

3. Now, in order to get the `prefect.yaml` file for deployment, prefect provides a command, run it in the terminal and choose **Store code on a local filesystem**.

    ```bash
    prefect init
    ```
    ![prefect_init_image](https://github.com/vatsalmpatel/dbt_project/blob/master/images/prefect_init.png)

4. Once you choose that, a template `prefect.yaml` file will appear in your directory. Open the file and fill in the necessary fields as seen in the `prefect.yaml` in this repo.

5. To create a **Prefect Deployment**, you will need to use the following command. When oyu run this command, it will automatically pick up the `prefect.yaml` and its configurations and create a deployment on the local Prefect Server, which will look something like the image below:

    ```bash
    prefect deploy
    ```
    ![prefect_deployment](https://github.com/vatsalmpatel/dbt_project/blob/master/images/prefect_deployment_run.png)

6. You will also need to start the worker pool that will listen for any pending/up-coming flows to run, without this, your deployment will not run> Mine runs on the created *deploy-pool*.

    ```bash
    prefect worker start --pool deploy-pool
    ```