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

    6. Finall create a schema in our database `dbt_db` using the role that we just created:

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

## Teardown and Cleanup:

- After you are done, you need to cleanup everything on snowflake, so that wwe do not incur any additional costs:

```sh
use role accountadmin;

drop warehouse if exists dbt_wh;
drop database if exists dbt_db;
drop role if exists dbt_role;
```