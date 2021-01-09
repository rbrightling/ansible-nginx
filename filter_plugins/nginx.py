""" Nginx Ansible Jinja Filters """
__metaclass__ = type

from ansible.parsing.yaml.objects import AnsibleUnicode


def option(value, join=" ", string=False):
    if value is True:
        return "on"
    elif value is False:
        return "off"
    elif type(value) is dict:
        parameter = option(value.pop('parameter'))
        item = []
        for key, val in value.items():
            if val is not None:
                item.append("{}={}".format(key, val))
        return "{} {}".format(parameter, " ".join(item))
    elif type(value) is list:
        if string:
            return '{}'.format(join.join([x if type(x) is AnsibleUnicode or type(x) is str else str(x) for x in value]))
        else:
            items = []
            for item in value:
                if type(item) is int or "=" in item:
                    items.append(str(item))
                else:
                    items.append('{}'.format(str(item)))
            return join.join(items)
    elif type(value) is AnsibleUnicode or type(value) is str:
        if " " in value:
            return '"{}"'.format(value.strip().replace('\n', '"\n    "'))
        else:
            return '{}'.format(value.strip().replace('\n', '\n    '))
    else:
        return value


def is_list_of_lists(value):
    if all(isinstance(v, list) for v in value):
        return True
    return False


class FilterModule(object):

    def filters(self):

        return {
            'nginx_option': option,
            'nginx_is_list_of_lists': is_list_of_lists
        }
