from prefect import flow, task
from prefect_dbt import DbtCliProfile
from dbt.cli.main import dbtRunner

@task
def run_dbt_command(command: str):
    dbt = dbtRunner()
    result = dbt.invoke(command.split())
    return result

@flow
def dbt_command_flow():
    commands = ['run','test']
    for command in commands:
        res = run_dbt_command(command)
        print(res)

if __name__ == "__main__":
    dbt_command_flow()