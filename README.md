Nginx
=====

![Test Ansible Role](https://github.com/rbrightling/ansible-nginx/workflows/Test%20Ansible%20Role/badge.svg?branch=main) [![Ansible Galaxy](http://img.shields.io/badge/galaxy-rbrightling.nginx-660198.svg?style=flat)](https://galaxy.ansible.com/rbrightling/nginx)

Install and configure Nginx web server. Configures both the global nginx configuration and an optional default site.

**NOTE**: Default site with ssl is provisioned for testing but should be provisioned seperately for production if used.


Requirements
------------

Supported OS's:
  - Debian 10
  - RedHat 8

Role Variables
--------------

Main variables for the nginx role
```yaml
# Deploy the default site files. Either from the role, overwritten with {{ playbook_dir}}/files/nginx/default_site, or
# false to manage with a different method.
nginx_manage_default_site_deploy: true
# Manage the default nginx config, false to manage with a different method.
nginx_manage_default_site_config: true

# Number of worker processes for nginx, best to set to CPU cores, auto tried to autodetect this.
nginx_worker_processes: auto

# Location of nginx's module config to include
nginx_include_modules: "{{ nginx__include_modules }}"
# Debian: "/etc/nginx/modules-enabled/*.conf"
# RedHat: "/usr/share/nginx/modules/*.conf"

# mime types config to load path
nginx_include_mime_types: /etc/nginx/mime.types

# Default mime type of a response.
nginx_default_type: application/octet-stream

# Nginx log settings
nginx_log_format_main: |
  $remote_addr - $remote_user [$time_local] '$request'
  $status $body_bytes_sent '$http_referer'
  '$http_user_agent' '$http_x_forwarded_for'
nginx_access_log: [/var/log/nginx/access.log, main]
nginx_error_log: [/var/log/nginx/error2.log, "{{ nginx_error_log_level }}"]
nginx_error_log_level: warn
nginx_log_not_found: false

# Maximum number of simultaneous connections that can be opened by a worker process.
nginx_worker_connections: 1024
# If multi_accept is disabled, a worker process will accept one new connection at a time.
nginx_multi_accept: true

# Enables or disables the use of sendfile().
# If tcp_nodelay & tcp_nopush are enabled uses nopush first, then nodelay for the last packet.
nginx_sendfile: true
# sets TCP_NODELAY flag, used on keepalive connections.
nginx_tcp_nodelay: true
# Optimise the amount of data sent simultaneously. (When using sendfile).
nginx_tcp_nopush: true

# Enables or disables the directory listing output.
nginx_autoindex: false

# Show nginx version in error pages and response headers.
nginx_server_tokens: false

# Adds the specified charset to the “Content-Type” response header field
nginx_charset: "utf-8"
# Sets the maximum size of the types hash tables.
nginx_types_hash_max_size: 2048

# SSL Certificate Settings
# ========================
nginx_ssl_certificate: "/etc/nginx/ssl/default/fullchain.pem"
nginx_ssl_certificate_key: "/etc/nginx/ssl/default/key.pem"

# Specifies a time during which a client may reuse the session parameters.
nginx_ssl_session_timeout: 1d
# Sets the types and sizes of caches that store session parameters.
nginx_ssl_session_cache: "shared:SSL:10m"
# Enables or disables session resumption through TLS session tickets.
nginx_ssl_session_tickets: false

# Enables the specified protocols.
nginx_ssl_protocols:
  - TLSv1.2
  - TLSv1.3

# Specifies the enabled ciphers.
nginx_ssl_ciphers:
  - ECDHE-ECDSA-AES128-GCM-SHA256
  - ECDHE-RSA-AES128-GCM-SHA256
  - ECDHE-ECDSA-AES256-GCM-SHA384
  - ECDHE-RSA-AES256-GCM-SHA384
  - ECDHE-ECDSA-CHACHA20-POLY1305
  - ECDHE-RSA-CHACHA20-POLY1305
  - DHE-RSA-AES128-GCM-SHA256
  - DHE-RSA-AES256-GCM-SHA384

# SSL dhparam path to generate if missing, set to false to not generate
nginx_ssl_dhparam: /etc/nginx/dhparam.pem
# Size of the dhparan
nginx_ssl_dhparam_size: 4096

# SSL Stapling
# ------------
nginx_ssl_stapling: true
nginx_ssl_stapling_verify: true
nginx_ssl_trusted_certificate: null
nginx_resolver:
  parameter:
    - 1.1.1.1
    - 1.0.0.1
    - 8.8.8.8
    - 8.8.4.4
    - 208.67.222.222
    - 208.67.220.220
  valid: 60s
nginx_resolver_timeout: 2s

# Size Limits & Buffer Overflows
nginx_client_body_buffer_size: 1k
nginx_client_header_buffer_size: 1k
nginx_client_max_body_size: 1k
nginx_large_client_header_buffers: [2, 1k]

# timeouts
nginx_client_body_timeout: 10
nginx_client_header_timeout: 10
nginx_keepalive_timeout: 5 5
nginx_send_timeout: 10

# GZip Compression
# ================
nginx_gzip: true
nginx_gzip_http_version: 1.1
nginx_gzip_disable: "msie6"
nginx_gzip_proxied: any
nginx_gzip_comp_level: 2
nginx_gzip_min_length: 1000
nginx_gzip_types:
  - text/plain
  - text/xml
  - text/css
  - applications/x-javascripts
  - applications/xml
nginx_gzip_vary: true

# Headers
# =======
nginx_add_headers_x_frame_options: "SAMEORIGIN"
nginx_add_headers_x_content_type_options: "nosniff"
nginx_add_headers_x_xss_protection: "1; mode=block"
nginx_add_headers_content_security_policy: "default-src 'self'"
nginx_add_headers_cache_control: "no-store"

# Extra Headers
nginx_add_headers: []
# Example:
#  - X-Frame-Options: "{{ nginx_add_headers_x_frame_options }}"
#  - X-Content-Type-Options: "{{ nginx_add_headers_x_content_type_options }}"
```

Variables for configuring the default site.
```yaml
nginx_default_server_http_state: redirect
nginx_default_server_https_state: enabled
# enabled: Enable the config block
# redirect: redirect to `nginx_default_server_redirect` with 301 code
# reject: return a 444 code
# disabled: remove the config block

# URL to rediect to, defaults to https of request
nginx_default_server_redirect: "https://$host$request_uri"

# Whitelist's IP's for rediect/reject codes, useful for monitoring.
nginx_default_server_remote_addr_whitelist: 127.0.0.1

# Allowed request methods
nginx_default_server_allow_request_methods:
  - GET
  - HEAD
  - POST

# HTTP port and listen
nginx_default_server_http_port: 80
nginx_default_server_http_listen:
  - ["{{ nginx_default_server_http_port }}", default_server]
  - ["[::]:{{ nginx_default_server_http_port }}", default_server]

# HTTPS port and listen
nginx_default_server_https_port: 443
nginx_default_server_https_listen:
  - ["{{ nginx_default_server_https_port }}", ssl, http2, default_server]
  - ["[::]:{{ nginx_default_server_https_port }}", ssl, http2, default_server]

# Directory to include for default site.
nginx_default_server_include: "/etc/nginx/default.d/*"

# root directory to be served from
nginx_default_server_root: "/srv/www/default"

# server_name for the default server
nginx_default_server_server_name: "_"
# Can take a single server name or list

# Default files for nginx to search to serve if not directly specified.
nginx_default_server_index: [index.html]

# Config location block for the directory sepcified with `nginx_default_server_location_root`.
nginx_default_server_location_root:
  - allow: "{{ nginx_default_server_allow }}"
  - deny: "{{ nginx_default_server_deny }}"
  - try_files: ["$uri", "$uri/", "=404" ]
nginx_default_server_allow: all
nginx_default_server_deny: null

# Addditional location blocks to be configured.
nginx_default_server_locations:
  - '~ ^/(images|javascript|js|css|flash|media|static)/':
    - expires: 7d
    - access_log: false
# Takes a list of values to create the location blocks and options. A dict of values are also converted (See add_header below)
# Example:
#  - '~ ^/path/':
#    - add_header:
#        x_frame_option: "ALLOW"
#        x_content_type_options: "nosniff"
# NOTE: if nginx add_header is set on a location it doesn't inherit previous  add_header declarations.


# Specify a SSL certfifcate/key to use for the default server
nginx_default_server_ssl_certificate: "{{ nginx_ssl_certificate }}"
nginx_default_server_ssl_certificate_key: "{{ nginx_ssl_certificate_key }}"

# Default server add_header options
nginx_default_server_add_header_x_frame_options: "DENY"
nginx_default_server_add_header_x_content_type_options: "nosniff"
nginx_default_server_add_header_x_xss_protection: "1; mode=block"
nginx_default_server_add_header_content_security_policy: "default-src 'self'"
nginx_default_server_add_header_cache_control: "public"
nginx_default_server_add_header_strict_transport_security: ["max-age=63072000", always] # HTTPS only
```

Dependencies
------------

None

Example Playbook
----------------

```yaml
- hosts: servers
  tasks:
    - name: include nginx role
      include_role:
        name: nginx
```

License
-------

LGPLv3

Author Information
------------------

- Robert Brightling | [GitLab](https://gitlab.com/brightling) | [GitHub](https://github.com/rbrightling)
