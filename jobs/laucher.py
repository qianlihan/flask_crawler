from flask_script import Command
import sys
import argparse
import traceback
import importlib
'''
how to run a job:
python manager.py runjob -m Test ( jobs/tasks/Test.py )
python manager.py runjob -m test/index ( jobs/tasks/test/index.py )
by default, jobs/tasks/...
'''


class runJob(Command):

    capture_all_args = True

    def run(self, *args, **kwargs):
        args = sys.argv[2:]
        parser = argparse.ArgumentParser(add_help=True)
        parser.add_argument("-m", "--name", dest="name",
                            metavar="name", help="job name", required=True)
        parser.add_argument("-a", "--act", dest="act",
                            metavar="act", help="job action", required=False)
        parser.add_argument("-p", "--param", dest="param", nargs="*",
                            metavar="param", help="job parameters", required=False)
        params = parser.parse_args(args)
        params_dict = params.__dict__
        if "name" not in params_dict or not params_dict['name']:
            return self.tips()

        try:
            '''
            For example,
            from jobs.tasks.test import JobTask
            '''
            module_name = params_dict['name'].replace("/", ".")
            import_string = "jobs.tasks." + module_name
            target = importlib.import_module(import_string)
            exit(target.JobTask().run(params_dict))
        except Exception as e:
            traceback.print_exc()
        return

        def tips(self):
            tip_msg = '''
            correct format is
            python3 manager.py runjob -m Test ( jobs/tasks/Test.py )
            python3 manager.py runjob -m test/index ( jobs/tasks/test/index.py )
            '''
            print(tip_msg)
            return
