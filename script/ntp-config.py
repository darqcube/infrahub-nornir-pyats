from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_netmiko.tasks import netmiko_send_config


def ntp_commands(task):
    commands = [
        "ntp server 216.239.35.12",
        "ntp source lo0",
        "ntp master 3",
        "do write memory",
    ]

    task.run(task=netmiko_send_config, config_commands=commands)


nr = InitNornir(config_file="config.yaml")
nr = nr.filter(name="ft-rc-r1")
result = nr.run(task=ntp_commands)
print_result(result)
