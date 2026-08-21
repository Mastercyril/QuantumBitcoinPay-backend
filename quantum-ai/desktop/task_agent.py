import os, json, threading, time, traceback
from datetime import datetime

class TaskAgent:
    def __init__(self):
        self.name = "TaskAgent"
        self.tasks = []
        self.completed = []
        self.failed = []
        self.running = False
        self.current_task = None
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.task_log_dir = os.path.join(base_dir, 'logs', 'tasks')
        os.makedirs(self.task_log_dir, exist_ok=True)

    def add_task(self, name, func, args=None, kwargs=None, priority=5):
        task = {
            'id': f'task_{len(self.tasks)+len(self.completed)+1:04d}',
            'name': name,
            'func': func,
            'args': args or [],
            'kwargs': kwargs or {},
            'priority': priority,
            'status': 'queued',
            'created': datetime.now().isoformat(),
            'started': None,
            'finished': None,
            'result': None,
            'error': None
        }
        self.tasks.append(task)
        self.tasks.sort(key=lambda x: x['priority'])
        print(f'[TaskAgent] Task queued: {name} (priority {priority})')
        return task['id']

    def execute_task(self, task):
        task['status'] = 'running'
        task['started'] = datetime.now().isoformat()
        self.current_task = task
        print(f'[TaskAgent] Executing: {task["name"]}')
        try:
            result = task['func'](*task['args'], **task['kwargs'])
            task['result'] = str(result) if result else 'completed'
            task['status'] = 'completed'
            task['finished'] = datetime.now().isoformat()
            self.completed.append(task)
            print(f'[TaskAgent] Completed: {task["name"]}')
        except Exception as e:
            task['error'] = str(e)
            task['status'] = 'failed'
            task['finished'] = datetime.now().isoformat()
            self.failed.append(task)
            print(f'[TaskAgent] Failed: {task["name"]} - {e}')
        self.current_task = None
        self._log_task(task)
        return task

    def _log_task(self, task):
        log_entry = {k: v for k, v in task.items() if k != 'func'}
        fname = f'{task["id"]}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        with open(os.path.join(self.task_log_dir, fname), 'w') as f:
            json.dump(log_entry, f, indent=2)

    def run_all(self):
        self.running = True
        print(f'[TaskAgent] Running {len(self.tasks)} tasks...')
        while self.tasks and self.running:
            task = self.tasks.pop(0)
            self.execute_task(task)
        self.running = False
        print(f'[TaskAgent] All tasks complete. Success: {len(self.completed)}, Failed: {len(self.failed)}')

    def run_async(self):
        t = threading.Thread(target=self.run_all, daemon=True)
        t.start()
        return t

    def stop(self):
        self.running = False
        print('[TaskAgent] Stop requested')

    def schedule_recurring(self, name, func, interval_seconds, args=None):
        def runner():
            while self.running:
                try:
                    func(*(args or []))
                except Exception as e:
                    print(f'[TaskAgent] Recurring task error: {e}')
                time.sleep(interval_seconds)
        self.running = True
        t = threading.Thread(target=runner, daemon=True)
        t.start()
        print(f'[TaskAgent] Recurring: {name} every {interval_seconds}s')
        return t

    def status(self):
        return {
            'engine': self.name,
            'queued': len(self.tasks),
            'completed': len(self.completed),
            'failed': len(self.failed),
            'running': self.running,
            'current': self.current_task['name'] if self.current_task else None
        }

if __name__ == "__main__":
    ta = TaskAgent()
    ta.add_task("Test Math", lambda: 2+2, priority=1)
    ta.add_task("Test String", lambda: "hello".upper(), priority=2)
    ta.add_task("Test List", lambda: list(range(10)), priority=3)
    ta.run_all()
    print(f"[TaskAgent] Status: {ta.status()}")
