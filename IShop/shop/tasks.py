from celery import shared_task
import time


@shared_task
def hello():
    time.sleep(10)
    print("Hello, world!")


@shared_task
def printer(n):
    for i in range(n):
        time.sleep(1)
        print(i + 1)
