import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


def test_nginx_installed(host):
    nginx_package_name = "nginx"
    nginx_package = host.package(nginx_package_name)
    assert nginx_package.is_installed


def test_nginx_service(host):
    service_name = "nginx"
    service = host.service(service_name)
    assert service.is_running
    assert service.is_enabled


def test_nginx_ports(host):
    port_list = [80, 443]
    for port in port_list:
        assert host.socket("tcp://0.0.0.0:{port}".format(port=port)).is_listening


def test_nginx_processes(host):
    master_nginx_process = host.process.get(user="root", comm="nginx")
    assert master_nginx_process.args.startswith("nginx: master process")
    workers = host.process.filter(ppid=master_nginx_process.pid)
    for worker in workers:
        assert worker.user == _get_distro_user_name(host.system_info.distribution)
        assert worker.args.startswith("nginx: worker process")


def test_nginx_conf_file(host):
    main_config = "/etc/nginx/nginx.conf"
    assert host.file(main_config).exists
    assert host.file(main_config).user == "root"
    assert host.file(main_config).group == "root"
    assert oct(host.file(main_config).mode) == "0o644"


def test_default_site_file(host):
    default_config = "/etc/nginx/sites-available/default"
    default_config_link = "/etc/nginx/sites-enabled/default"
    assert host.file(default_config).exists
    assert host.file(default_config).is_file
    assert host.file(default_config).user == "root"
    assert host.file(default_config).group == "root"
    assert oct(host.file(default_config).mode) == "0o644"
    assert host.file(default_config_link).exists
    assert host.file(default_config_link).is_symlink
    assert host.file(default_config_link).user == "root"
    assert host.file(default_config_link).group == "root"


def test_default_request(host):
    http_request = host.command.check_output("curl 127.0.0.1")
    https_request = host.command.check_output("curl --insecure https://127.0.0.1")
    html = "<title>Default Webpage</title>"
    assert html in http_request
    assert html in https_request


def test_default_header(host):
    https_headers = host.command.check_output("curl --head --insecure https://127.0.0.1")
    assert "x-frame-options: DENY" in https_headers
    assert "x-content-type-options: nosniff" in https_headers
    assert "x-xss-protection: 1; mode=block" in https_headers
    assert "content-security-policy: default-src 'self'" in https_headers
    assert "strict-transport-security: max-age=63072000" in https_headers
    assert "server: nginx" in https_headers


def _get_distro_user_name(host_distro):
    return {
        "centos": "nginx",
        "debian": "www-data"
    }.get(host_distro, "nginx")
