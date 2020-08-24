# See https://github.com/PrefectHQ/prefect/issues/2322
from prefect import Flow, task


@task
def numbers_task():
    return [1, 2, 3]


@task
def map_task(x):
    return x + 1


@task
def reduce_task(x):
    return sum(x)


with Flow("MapReduce") as flow:
    numbers = numbers_task()
    first_map = map_task.map(numbers)
    second_map = map_task.map(first_map)
    reduction = reduce_task(second_map)


if __name__ == "__main__":
    flow.register(project_name="MapReduce")
    flow.run_agent()
