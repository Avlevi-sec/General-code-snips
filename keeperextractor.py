from keepercommander import api
from keepercommander.commands.enterprise import UserReportCommand, SecurityAuditReportCommand
from keepercommander.params import KeeperParams

my_params = KeeperParams()
my_params.user = "user@company.com"
my_params.password = password"

api.login(my_params)
api.sync_down(my_params)

#searches password based on name and returns a list of matching records
# result = api.search_records(my_params,"orca")
# print(vars(result[0]))

#searches password based on ID and thats it
# record = api.get_record(my_params,"uuokWQH1slUXKvyZuTLhZg")
# print(vars(record))
