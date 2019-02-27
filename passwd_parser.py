import sys
import json


class User:

    def __init__(self, uid, full_name, groups):
        self.uid = uid
        self.full_name = full_name
        self.groups = groups

    def __iter__(self):
        yield 'uid', self.uid
        yield 'full_name', self.full_name
        yield 'groups', self.groups


def read_files_and_get_map(password_file, groups_file):
    password_file_content = [line.rstrip('\n') for line in open(password_file)]
    groups_file_content = [line.rstrip('\n') for line in open(groups_file)]
    result, groups_dict = dict(), dict()
    for line in groups_file_content:
        line = line.split(":")
        groups_dict[line[2]] = line[0]
    for line in password_file_content:
        line = line.split(":")
        group_id = line[3]
        group = []
        if group_id in groups_dict:
            group.append(groups_dict[group_id])
        result[line[0]] = dict(User(line[2], line[4], group))
    for line in groups_file_content:
        line = line.split(":")
        users_list = line[3].split(",")
        for user in users_list:
            if user in result:
                user_obj = result[user]
                if line[0] not in user_obj["groups"]:
                    user_obj["groups"].append(line[0])
                result[user] = user_obj
    return result


if __name__ == "__main__":
    passwordFile = "/etc/passwd"
    groupsFile = "/etc/groups"
    if len(sys.argv) >= 3:
        passwordFile = sys.argv[1]
        groupsFile = sys.argv[2]
    try:
        print(json.dumps(read_files_and_get_map(passwordFile, groupsFile), indent=2))
    except (OSError, IOError, IndexError) as e:
        print("\nPlease enter valid file names in below format!")
        print("#######################################################################")
        print("python passwd_parser.py <path-to-password-file> <path-to-groups-file>")
        print("#######################################################################\n")
