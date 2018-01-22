from ansible.executor.task_queue_manager import TaskQueueManager

from ansible.executor import playbook_executor

from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager

from ansible.inventory.manager import InventoryManager

from ansible.utils.display import Display

from ansible.playbook import Playbook

from collections import namedtuple

from ansible.plugins.callback.json import CallbackModule as jsCB

inv_source = "/home/zml/python/tansible/playbook/inventory/test"

loader = DataLoader()
loader.set_basedir("/home/zml/python/tansible/playbook")
print(loader.get_basedir())
inventory = InventoryManager(loader, inv_source)
variable_manager = VariableManager(loader, inventory)


class Option():
    pass


display = Display(1)

# opt = Option()
# opt.config_file = "/home/zml/python/tansible/playbook/ansible.cfg"
# opt.listhosts = None
# opt.listtasks = None
# opt.listtags = None
# opt.syntax = None

# opt.display = Display(10)
# # opt.display.verbosity = 10
# opt.verbosity = 10

# playbook_executor.verbosity = 10

# opt.module_path = None
# opt.become = None
# opt.become_method = None
# opt.become_user = "root"

# opt.check = None
# opt.diff = None
# opt.forks = 1
# opt.remote_user = 'root'
    
# opt.connection='ssh'



Options = namedtuple('Options', [
    'listtags', 'listtasks', 'listhosts', 'syntax', 'connection',
    'module_path', 'forks', 'remote_user', 'private_key_file',
    'ssh_common_args', 'ssh_extra_args', 'sftp_extra_args', 'scp_extra_args',
    'become', 'become_method', 'become_user', 'verbosity', 'check', "diff"
])
options = Options(
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


playbook = ["/home/zml/python/tansible/playbook/test.yml"]


pb = Playbook.load(playbook[0], variable_manager=variable_manager, loader=loader)

print(pb)

play = pb.get_plays()[0]

# pbex = playbook_executor.PlaybookExecutor(playbook, inventory,
#                                           variable_manager, loader, options, {})

# result = pbex.run()

passwords = {}


jcb = jsCB()
tqm = TaskQueueManager(
        inventory=inventory,
        variable_manager=variable_manager,
        loader=loader,
        options=options,
        passwords=passwords,
        stdout_callback=jcb,
    )

result = tqm.run(play)

print("OK------")

print(inventory.get_hosts())

stats = tqm._stats
tqm.cleanup()

print(result)
print(stats)
hosts = sorted(stats.processed.keys())
for h in inventory.hosts:
    print(h)
    print(type(h))
    print(stats.summarize(h))

print(stats.summarize("csbjjmp"))

print(jcb.results)