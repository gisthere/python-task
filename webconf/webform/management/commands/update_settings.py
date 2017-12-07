from django.core.management.base import BaseCommand
from webform.models import Label

from python_hosts import Hosts, HostsEntry
import os
from tempfile import NamedTemporaryFile


httpd_conf = "/etc/httpd/conf.d/httpd.conf"


def update_hosts(addr, server_name):
    my_hosts = Hosts()
    new_entry = HostsEntry(entry_type='ipv4', address=addr, names=[server_name])
    my_hosts.add([new_entry])
    my_hosts.write()


def update_httpd_conf(addr, port, server_name, document_root):
    with open(httpd_conf) as fin, NamedTemporaryFile() as fout:
        for line in fin:
            if line.startswith("Listen "):
                line = "Listen {addr}:{port}\n".format(addr=addr, port=port)
            elif line.startswith("ServerName "):
                line = "ServerName {server_name}:{port}\n".format(server_name=server_name, port=port)
            elif line.startswith("DocumentRoot "):
                line = "DocumentRoot \"{document_root}\"\n".format(document_root=document_root)
            fout.write(line.encode('utf8'))
        os.unlink(httpd_conf)
        os.link(fout.name, httpd_conf)


class Command(BaseCommand):
    help = 'Update settings'

    def handle(self, *args, **options):
        labels = ('ServerName', 'Host', 'Port', 'DocumentRoot')
        settings = dict()
        for l in labels:
            v = Label.objects.get(key=l).value
            settings[l] = v

        update_hosts(settings['Host'], settings['ServerName'])
        update_httpd_conf(settings['Host'], settings['Port'], settings['ServerName'], settings['DocumentRoot'])
        os.system("systemctl restart httpd")

