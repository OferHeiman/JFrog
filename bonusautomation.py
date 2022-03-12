import rtpy
# rtpy documentation: https://rtpy.readthedocs.io/en/latest/index.html

# instantiate a rtpy.Rtpy object
settings = {}
settings["af_url"] = "http://localhost:8082/artifactory"
settings["username"] = "admin"
settings["password"] = "Aa123456789"
af = rtpy.Rtpy(settings)

# ping
ping = af.system_and_configuration.system_health_ping()
print(ping)


#get repositories
print("repositories before adding new teams:")
repositories = af.repositories.get_repositories()
for repository in repositories:
    print(repository)

# #get users
print("users before adding new teams:")
users = af.security.get_users()
for user in users:
    print(user)

team_number = int(input("Choose first team number: "))
virtual_repository_name = "virtual_repository_teams_"+str(team_number)+"_and_"+str(team_number+1)
shared_repository_name = "shared_local_repository_teams_"+str(team_number)+"_and_"+str(team_number+1)
# 1.Created a virtual repository.
params = {}
params["key"] = virtual_repository_name
params["rclass"] = "virtual"
params["packageType"] = "generic"
create_repo = af.repositories.create_repository(params)

# 2.Created two users with admin access(managers), one for each team.
params = {}
for x in range(2):
    params["name"] = "team"+str(x+team_number)+"manager"
    params["admin"] = "true"
    params["email"] = "team"+str(x+team_number)+"manager"+"@gmail.com"
    params["password"] = "Aa123456789"
    create_user = af.security.create_or_replace_user(params)

# 3.Created two developers users for each team with the ability to manage resources(user details file doesn't include 'resourcesManager' parameter?), created a local repository for each team.
#create users for each team
params = {}
for y in range(2):
    for x in range(2):
        params["name"] = "team"+str(x+team_number)+"developer"+str(y+1)
        params["resourcesManager"] = "true"
        params["admin"] = "false"
        params["email"] = "team"+str(x+team_number)+"developer"+str(y+1)+"@gmail.com"
        params["password"] = "Aa123456789"
        create_user = af.security.create_or_replace_user(params)
#create local repository for each team
params = {}
for x in range(2):
    params["key"] = "team"+str(x+team_number)+"_local_repository"
    params["rclass"] = "local"
    params["packageType"] = "generic"
    create_repo = af.repositories.create_repository(params)

#4.Created permissions for users on team1 to access team1's local repository, and also created permissions for users on team2 to access team2's local repository.
params = {}
for x in range(2):
    params["name"] = "team"+str(x+team_number)+"_permissions"
    params["repositories"] = ["team"+str(x+team_number)+"_local_repository"]
    params["principals"] = {'users': {'team' + str(x + team_number) + 'developer2': ['r', 'mxm', 'd', 'w', 'n'],
                                      'team' + str(x + team_number) + 'developer1': ['r', 'mxm', 'd', 'w', 'n']}}
    r = af.security.create_or_replace_permission_target(params)

#5.Artifacts of both teams will appear in the virtual shared repository.
params = {}
params["key"] = virtual_repository_name
params["repositories"] = ["team"+str(team_number)+"_local_repository", "team"+str(team_number+1)+"_local_repository"]
r = af.repositories.update_repository_configuration(params)

#6.Created a shared local repository, edited the permissions to allow both teams to access the shared local repository.
#create new shared local repository
params = {}
params["key"] = shared_repository_name
params["rclass"] = "local"
params["packageType"] = "generic"
create_repo = af.repositories.create_repository(params)
#add new shared local repository to virtual repository
params = {}
params["key"] = virtual_repository_name
params["repositories"] = ["team"+str(team_number)+"_local_repository", "team"+str(team_number+1)+"_local_repository", virtual_repository_name]
r = af.repositories.update_repository_configuration(params)
#update permissions, both teams will be able to access the new shared local repository
params = {}
for x in range(2):
    params["name"] = "team"+str(x+team_number)+"_permissions"
    params["repositories"] = ["team"+str(x+team_number)+"_local_repository", shared_repository_name]
    params["principals"] = {'users': {'team' + str(x + team_number) + 'developer2': ['r', 'mxm', 'd', 'w', 'n'],
                                      'team' + str(x + team_number) + 'developer1': ['r', 'mxm', 'd', 'w', 'n']}}
    r = af.security.create_or_replace_permission_target(params)

#get repositories
print("repositories after adding new teams:")
repositories = af.repositories.get_repositories()
for repository in repositories:
    print(repository)

# #get users
print("users after adding new teams:")
users = af.security.get_users()
for user in users:
    print(user)