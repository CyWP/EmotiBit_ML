import asyncio

class TaskManager:
    _tasks = []

    @classmethod
    def register_task(cls, task):
        cls._tasks.append(task)

    @classmethod
    async def run_tasks(cls):
        await asyncio.gather(*cls._tasks)

    @classmethod
    async def cancel_tasks(cls):
        for task in cls._tasks:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass