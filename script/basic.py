from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_netmiko.tasks import netmiko_send_command


# def say_hello(task):
# return (
#     f"My Task Works! Yaay {task.host} - {task.host.groups} - {task.host.hostname}"
# )


nr = InitNornir(config_file="config.yaml")
result = nr.run(task=netmiko_send_command, command_string="show config | sec ntp")
print_result(result)
