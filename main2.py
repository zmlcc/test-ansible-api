from ansible.executor.task_queue_manager import TaskQueueManager

from ansible.playbook import Playbook
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager

from ansible.inventory.manager import InventoryManager

from ansible.utils.display import Display


from collections import namedtuple

from ansible.plugins.callback.json import CallbackModule as jsCB

inv_source = "/home/zml/python/tansible/playbook/inventory/test"

playbook = "/home/zml/python/tansible/playbook/test.yml"
basedir = "/home/zml/python/tansible/playbook"

display = Display(0)

Options = namedtuple('Options', [
    'listtags', 'listtasks', 'listhosts', 'syntax', 'connection',
    'module_path', 'forks', 'remote_user', 'private_key_file',
    'ssh_common_args', 'ssh_extra_args', 'sftp_extra_args', 'scp_extra_args',
    'become', 'become_method', 'become_user', 'verbosity', 'check', "diff"
])



def run_playbook(playbook, inv, basedir, option=None):
    if option is None:
        option = Options(
            listtags=False,
            listtasks=False,
            listhosts=False,
            syntax=False,
            connection='ssh',
            module_path=None,
            forks=100,
            remote_user='root',
            private_key_file=None,
            ssh_common_args=None,
            ssh_extra_args=None,
            sftp_extra_args=None,
            scp_extra_args=None,
            become=True,
            become_method=None,
            become_user='root',
            verbosity=10,
            check=False,
            diff=None)

    loader = DataLoader()
    loader.set_basedir(basedir)
    inventory = InventoryManager(loader, inv)
    variable_manager = VariableManager(loader, inventory)

    pb = Playbook.load(playbook, variable_manager=variable_manager, loader=loader)
    play = pb.get_plays()[0]

    passwd = {}
    jcb = jsCB()

    tqm = TaskQueueManager(
        inventory=inventory,
        variable_manager=variable_manager,
        loader=loader,
        options=option,
        passwords=passwd,
        stdout_callback=jcb,
    )

    tqm.run(play) 
    tqm.cleanup()
    
    stats = [(h, tqm._stats.summarize(h)) for h in inventory.hosts]

    return stats, jcb.results


stat, result = run_playbook(playbook, inv_source, basedir)

print(stat)
print(result)
    