#!/usr/bin/python3
"""
Postgres Client for unit testing
Transmits (plays) client (psql or Power BI) pre-recorded messages sequentialy for unit testing the pg_server_proxy module   
TCP Client example taken from: https://gist.github.com/homoluctus/5ee21411dd89cebbb237b51ab56f0a4c

Running psql from Windows PowerShell : 
<power shell> & 'C:\Program Files\PostgreSQL\13\bin\psql.exe' "dbname=postgres user=postgres sslmode=disable"
"""

import logging
logging.basicConfig(level=logging.DEBUG)

import socket

# Power BI sequence of messages
PBI_STARTUP_MSG_1 = b'\x00\x00\x00>\x00\x03\x00\x00user\x00postgres\x00client_encoding\x00UTF8\x00database\x00postgres\x00\x00'
PBI_PASSWORD_MSG_2 = b'p\x00\x00\x00(md5b400a301a6904ae12fc76a8fff168215\x00'
PBI_PBDES_MSG_3 = b"P\x00\x00\x00\xb6\x00select TABLE_SCHEMA, TABLE_NAME, TABLE_TYPE\r\nfrom INFORMATION_SCHEMA.tables\r\nwhere TABLE_SCHEMA not in ('information_schema', 'pg_catalog')\r\norder by TABLE_SCHEMA, TABLE_NAME\x00\x00\x00B\x00\x00\x00\x0e\x00\x00\x00\x00\x00\x00\x00\x01\x00\x01D\x00\x00\x00\x06P\x00E\x00\x00\x00\t\x00\x00\x00\x00\x00S\x00\x00\x00\x04"
PBI_PBDE_x3_S = b"\x50\x00\x00\x06" \
b"\xc0\x00\x0d\x0a\x2f\x2a\x2a\x2a\x20\x4c\x6f\x61\x64\x20\x61\x6c" \
b"\x6c\x20\x73\x75\x70\x70\x6f\x72\x74\x65\x64\x20\x74\x79\x70\x65" \
b"\x73\x20\x2a\x2a\x2a\x2f\x0d\x0a\x53\x45\x4c\x45\x43\x54\x20\x6e" \
b"\x73\x2e\x6e\x73\x70\x6e\x61\x6d\x65\x2c\x20\x61\x2e\x74\x79\x70" \
b"\x6e\x61\x6d\x65\x2c\x20\x61\x2e\x6f\x69\x64\x2c\x20\x61\x2e\x74" \
b"\x79\x70\x72\x65\x6c\x69\x64\x2c\x20\x61\x2e\x74\x79\x70\x62\x61" \
b"\x73\x65\x74\x79\x70\x65\x2c\x0d\x0a\x43\x41\x53\x45\x20\x57\x48" \
b"\x45\x4e\x20\x70\x67\x5f\x70\x72\x6f\x63\x2e\x70\x72\x6f\x6e\x61" \
b"\x6d\x65\x3d\x27\x61\x72\x72\x61\x79\x5f\x72\x65\x63\x76\x27\x20" \
b"\x54\x48\x45\x4e\x20\x27\x61\x27\x20\x45\x4c\x53\x45\x20\x61\x2e" \
b"\x74\x79\x70\x74\x79\x70\x65\x20\x45\x4e\x44\x20\x41\x53\x20\x74" \
b"\x79\x70\x65\x2c\x0d\x0a\x43\x41\x53\x45\x0d\x0a\x20\x20\x57\x48" \
b"\x45\x4e\x20\x70\x67\x5f\x70\x72\x6f\x63\x2e\x70\x72\x6f\x6e\x61" \
b"\x6d\x65\x3d\x27\x61\x72\x72\x61\x79\x5f\x72\x65\x63\x76\x27\x20" \
b"\x54\x48\x45\x4e\x20\x61\x2e\x74\x79\x70\x65\x6c\x65\x6d\x0d\x0a" \
b"\x20\x20\x57\x48\x45\x4e\x20\x61\x2e\x74\x79\x70\x74\x79\x70\x65" \
b"\x3d\x27\x72\x27\x20\x54\x48\x45\x4e\x20\x72\x6e\x67\x73\x75\x62" \
b"\x74\x79\x70\x65\x0d\x0a\x20\x20\x45\x4c\x53\x45\x20\x30\x0d\x0a" \
b"\x45\x4e\x44\x20\x41\x53\x20\x65\x6c\x65\x6d\x6f\x69\x64\x2c\x0d" \
b"\x0a\x43\x41\x53\x45\x0d\x0a\x20\x20\x57\x48\x45\x4e\x20\x70\x67" \
b"\x5f\x70\x72\x6f\x63\x2e\x70\x72\x6f\x6e\x61\x6d\x65\x20\x49\x4e" \
b"\x20\x28\x27\x61\x72\x72\x61\x79\x5f\x72\x65\x63\x76\x27\x2c\x27" \
b"\x6f\x69\x64\x76\x65\x63\x74\x6f\x72\x72\x65\x63\x76\x27\x29\x20" \
b"\x54\x48\x45\x4e\x20\x33\x20\x20\x20\x20\x2f\x2a\x20\x41\x72\x72" \
b"\x61\x79\x73\x20\x6c\x61\x73\x74\x20\x2a\x2f\x0d\x0a\x20\x20\x57" \
b"\x48\x45\x4e\x20\x61\x2e\x74\x79\x70\x74\x79\x70\x65\x3d\x27\x72" \
b"\x27\x20\x54\x48\x45\x4e\x20\x32\x20\x20\x20\x20\x20\x20\x20\x20" \
b"\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20" \
b"\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20" \
b"\x2f\x2a\x20\x52\x61\x6e\x67\x65\x73\x20\x62\x65\x66\x6f\x72\x65" \
b"\x20\x2a\x2f\x0d\x0a\x20\x20\x57\x48\x45\x4e\x20\x61\x2e\x74\x79" \
b"\x70\x74\x79\x70\x65\x3d\x27\x64\x27\x20\x54\x48\x45\x4e\x20\x31" \
b"\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20" \
b"\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20" \
b"\x20\x20\x20\x20\x20\x20\x20\x20\x2f\x2a\x20\x44\x6f\x6d\x61\x69" \
b"\x6e\x73\x20\x62\x65\x66\x6f\x72\x65\x20\x2a\x2f\x0d\x0a\x20\x20" \
b"\x45\x4c\x53\x45\x20\x30\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20" \
b"\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20" \
b"\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20" \
b"\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20" \
b"\x20\x2f\x2a\x20\x42\x61\x73\x65\x20\x74\x79\x70\x65\x73\x20\x66" \
b"\x69\x72\x73\x74\x20\x2a\x2f\x0d\x0a\x45\x4e\x44\x20\x41\x53\x20" \
b"\x6f\x72\x64\x0d\x0a\x46\x52\x4f\x4d\x20\x70\x67\x5f\x74\x79\x70" \
b"\x65\x20\x41\x53\x20\x61\x0d\x0a\x4a\x4f\x49\x4e\x20\x70\x67\x5f" \
b"\x6e\x61\x6d\x65\x73\x70\x61\x63\x65\x20\x41\x53\x20\x6e\x73\x20" \
b"\x4f\x4e\x20\x28\x6e\x73\x2e\x6f\x69\x64\x20\x3d\x20\x61\x2e\x74" \
b"\x79\x70\x6e\x61\x6d\x65\x73\x70\x61\x63\x65\x29\x0d\x0a\x4a\x4f" \
b"\x49\x4e\x20\x70\x67\x5f\x70\x72\x6f\x63\x20\x4f\x4e\x20\x70\x67" \
b"\x5f\x70\x72\x6f\x63\x2e\x6f\x69\x64\x20\x3d\x20\x61\x2e\x74\x79" \
b"\x70\x72\x65\x63\x65\x69\x76\x65\x0d\x0a\x4c\x45\x46\x54\x20\x4f" \
b"\x55\x54\x45\x52\x20\x4a\x4f\x49\x4e\x20\x70\x67\x5f\x63\x6c\x61" \
b"\x73\x73\x20\x41\x53\x20\x63\x6c\x73\x20\x4f\x4e\x20\x28\x63\x6c" \
b"\x73\x2e\x6f\x69\x64\x20\x3d\x20\x61\x2e\x74\x79\x70\x72\x65\x6c" \
b"\x69\x64\x29\x0d\x0a\x4c\x45\x46\x54\x20\x4f\x55\x54\x45\x52\x20" \
b"\x4a\x4f\x49\x4e\x20\x70\x67\x5f\x74\x79\x70\x65\x20\x41\x53\x20" \
b"\x62\x20\x4f\x4e\x20\x28\x62\x2e\x6f\x69\x64\x20\x3d\x20\x61\x2e" \
b"\x74\x79\x70\x65\x6c\x65\x6d\x29\x0d\x0a\x4c\x45\x46\x54\x20\x4f" \
b"\x55\x54\x45\x52\x20\x4a\x4f\x49\x4e\x20\x70\x67\x5f\x63\x6c\x61" \
b"\x73\x73\x20\x41\x53\x20\x65\x6c\x65\x6d\x63\x6c\x73\x20\x4f\x4e" \
b"\x20\x28\x65\x6c\x65\x6d\x63\x6c\x73\x2e\x6f\x69\x64\x20\x3d\x20" \
b"\x62\x2e\x74\x79\x70\x72\x65\x6c\x69\x64\x29\x0d\x0a\x4c\x45\x46" \
b"\x54\x20\x4f\x55\x54\x45\x52\x20\x4a\x4f\x49\x4e\x20\x70\x67\x5f" \
b"\x72\x61\x6e\x67\x65\x20\x4f\x4e\x20\x28\x70\x67\x5f\x72\x61\x6e" \
b"\x67\x65\x2e\x72\x6e\x67\x74\x79\x70\x69\x64\x20\x3d\x20\x61\x2e" \
b"\x6f\x69\x64\x29\x20\x0d\x0a\x57\x48\x45\x52\x45\x0d\x0a\x20\x20" \
b"\x61\x2e\x74\x79\x70\x74\x79\x70\x65\x20\x49\x4e\x20\x28\x27\x62" \
b"\x27\x2c\x20\x27\x72\x27\x2c\x20\x27\x65\x27\x2c\x20\x27\x64\x27" \
b"\x29\x20\x4f\x52\x20\x20\x20\x20\x20\x20\x20\x20\x20\x2f\x2a\x20" \
b"\x42\x61\x73\x65\x2c\x20\x72\x61\x6e\x67\x65\x2c\x20\x65\x6e\x75" \
b"\x6d\x2c\x20\x64\x6f\x6d\x61\x69\x6e\x20\x2a\x2f\x0d\x0a\x20\x20" \
b"\x28\x61\x2e\x74\x79\x70\x74\x79\x70\x65\x20\x3d\x20\x27\x63\x27" \
b"\x20\x41\x4e\x44\x20\x63\x6c\x73\x2e\x72\x65\x6c\x6b\x69\x6e\x64" \
b"\x3d\x27\x63\x27\x29\x20\x4f\x52\x20\x2f\x2a\x20\x55\x73\x65\x72" \
b"\x2d\x64\x65\x66\x69\x6e\x65\x64\x20\x66\x72\x65\x65\x2d\x73\x74" \
b"\x61\x6e\x64\x69\x6e\x67\x20\x63\x6f\x6d\x70\x6f\x73\x69\x74\x65" \
b"\x73\x20\x28\x6e\x6f\x74\x20\x74\x61\x62\x6c\x65\x20\x63\x6f\x6d" \
b"\x70\x6f\x73\x69\x74\x65\x73\x29\x20\x62\x79\x20\x64\x65\x66\x61" \
b"\x75\x6c\x74\x20\x2a\x2f\x0d\x0a\x20\x20\x28\x70\x67\x5f\x70\x72" \
b"\x6f\x63\x2e\x70\x72\x6f\x6e\x61\x6d\x65\x3d\x27\x61\x72\x72\x61" \
b"\x79\x5f\x72\x65\x63\x76\x27\x20\x41\x4e\x44\x20\x28\x0d\x0a\x20" \
b"\x20\x20\x20\x62\x2e\x74\x79\x70\x74\x79\x70\x65\x20\x49\x4e\x20" \
b"\x28\x27\x62\x27\x2c\x20\x27\x72\x27\x2c\x20\x27\x65\x27\x2c\x20" \
b"\x27\x64\x27\x29\x20\x4f\x52\x20\x20\x20\x20\x20\x20\x20\x2f\x2a" \
b"\x20\x41\x72\x72\x61\x79\x20\x6f\x66\x20\x62\x61\x73\x65\x2c\x20" \
b"\x72\x61\x6e\x67\x65\x2c\x20\x65\x6e\x75\x6d\x2c\x20\x64\x6f\x6d" \
b"\x61\x69\x6e\x20\x2a\x2f\x0d\x0a\x20\x20\x20\x20\x28\x62\x2e\x74" \
b"\x79\x70\x74\x79\x70\x65\x20\x3d\x20\x27\x70\x27\x20\x41\x4e\x44" \
b"\x20\x62\x2e\x74\x79\x70\x6e\x61\x6d\x65\x20\x49\x4e\x20\x28\x27" \
b"\x72\x65\x63\x6f\x72\x64\x27\x2c\x20\x27\x76\x6f\x69\x64\x27\x29" \
b"\x29\x20\x4f\x52\x20\x2f\x2a\x20\x41\x72\x72\x61\x79\x73\x20\x6f" \
b"\x66\x20\x73\x70\x65\x63\x69\x61\x6c\x20\x73\x75\x70\x70\x6f\x72" \
b"\x74\x65\x64\x20\x70\x73\x65\x75\x64\x6f\x2d\x74\x79\x70\x65\x73" \
b"\x20\x2a\x2f\x0d\x0a\x20\x20\x20\x20\x28\x62\x2e\x74\x79\x70\x74" \
b"\x79\x70\x65\x20\x3d\x20\x27\x63\x27\x20\x41\x4e\x44\x20\x65\x6c" \
b"\x65\x6d\x63\x6c\x73\x2e\x72\x65\x6c\x6b\x69\x6e\x64\x3d\x27\x63" \
b"\x27\x29\x20\x20\x2f\x2a\x20\x41\x72\x72\x61\x79\x20\x6f\x66\x20" \
b"\x75\x73\x65\x72\x2d\x64\x65\x66\x69\x6e\x65\x64\x20\x66\x72\x65" \
b"\x65\x2d\x73\x74\x61\x6e\x64\x69\x6e\x67\x20\x63\x6f\x6d\x70\x6f" \
b"\x73\x69\x74\x65\x73\x20\x28\x6e\x6f\x74\x20\x74\x61\x62\x6c\x65" \
b"\x20\x63\x6f\x6d\x70\x6f\x73\x69\x74\x65\x73\x29\x20\x2a\x2f\x0d" \
b"\x0a\x20\x20\x29\x29\x20\x4f\x52\x0d\x0a\x20\x20\x28\x61\x2e\x74" \
b"\x79\x70\x74\x79\x70\x65\x20\x3d\x20\x27\x70\x27\x20\x41\x4e\x44" \
b"\x20\x61\x2e\x74\x79\x70\x6e\x61\x6d\x65\x20\x49\x4e\x20\x28\x27" \
b"\x72\x65\x63\x6f\x72\x64\x27\x2c\x20\x27\x76\x6f\x69\x64\x27\x29" \
b"\x29\x20\x20\x2f\x2a\x20\x53\x6f\x6d\x65\x20\x73\x70\x65\x63\x69" \
b"\x61\x6c\x20\x73\x75\x70\x70\x6f\x72\x74\x65\x64\x20\x70\x73\x65" \
b"\x75\x64\x6f\x2d\x74\x79\x70\x65\x73\x20\x2a\x2f\x0d\x0a\x4f\x52" \
b"\x44\x45\x52\x20\x42\x59\x20\x6f\x72\x64\x00\x00\x00\x42\x00\x00" \
b"\x00\x0e\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x44\x00\x00\x00" \
b"\x06\x50\x00\x45\x00\x00\x00\x09\x00\x00\x00\x00\x00\x50\x00\x00" \
b"\x01\xd2\x00\x2f\x2a\x2a\x2a\x20\x4c\x6f\x61\x64\x20\x66\x69\x65" \
b"\x6c\x64\x20\x64\x65\x66\x69\x6e\x69\x74\x69\x6f\x6e\x73\x20\x66" \
b"\x6f\x72\x20\x28\x66\x72\x65\x65\x2d\x73\x74\x61\x6e\x64\x69\x6e" \
b"\x67\x29\x20\x63\x6f\x6d\x70\x6f\x73\x69\x74\x65\x20\x74\x79\x70" \
b"\x65\x73\x20\x2a\x2a\x2a\x2f\x0d\x0a\x53\x45\x4c\x45\x43\x54\x20" \
b"\x74\x79\x70\x2e\x6f\x69\x64\x2c\x20\x61\x74\x74\x2e\x61\x74\x74" \
b"\x6e\x61\x6d\x65\x2c\x20\x61\x74\x74\x2e\x61\x74\x74\x74\x79\x70" \
b"\x69\x64\x0d\x0a\x46\x52\x4f\x4d\x20\x70\x67\x5f\x74\x79\x70\x65" \
b"\x20\x41\x53\x20\x74\x79\x70\x0d\x0a\x4a\x4f\x49\x4e\x20\x70\x67" \
b"\x5f\x6e\x61\x6d\x65\x73\x70\x61\x63\x65\x20\x41\x53\x20\x6e\x73" \
b"\x20\x4f\x4e\x20\x28\x6e\x73\x2e\x6f\x69\x64\x20\x3d\x20\x74\x79" \
b"\x70\x2e\x74\x79\x70\x6e\x61\x6d\x65\x73\x70\x61\x63\x65\x29\x0d" \
b"\x0a\x4a\x4f\x49\x4e\x20\x70\x67\x5f\x63\x6c\x61\x73\x73\x20\x41" \
b"\x53\x20\x63\x6c\x73\x20\x4f\x4e\x20\x28\x63\x6c\x73\x2e\x6f\x69" \
b"\x64\x20\x3d\x20\x74\x79\x70\x2e\x74\x79\x70\x72\x65\x6c\x69\x64" \
b"\x29\x0d\x0a\x4a\x4f\x49\x4e\x20\x70\x67\x5f\x61\x74\x74\x72\x69" \
b"\x62\x75\x74\x65\x20\x41\x53\x20\x61\x74\x74\x20\x4f\x4e\x20\x28" \
b"\x61\x74\x74\x2e\x61\x74\x74\x72\x65\x6c\x69\x64\x20\x3d\x20\x74" \
b"\x79\x70\x2e\x74\x79\x70\x72\x65\x6c\x69\x64\x29\x0d\x0a\x57\x48" \
b"\x45\x52\x45\x0d\x0a\x20\x20\x28\x74\x79\x70\x2e\x74\x79\x70\x74" \
b"\x79\x70\x65\x20\x3d\x20\x27\x63\x27\x20\x41\x4e\x44\x20\x63\x6c" \
b"\x73\x2e\x72\x65\x6c\x6b\x69\x6e\x64\x3d\x27\x63\x27\x29\x20\x41" \
b"\x4e\x44\x0d\x0a\x20\x20\x61\x74\x74\x6e\x75\x6d\x20\x3e\x20\x30" \
b"\x20\x41\x4e\x44\x20\x20\x20\x20\x20\x2f\x2a\x20\x44\x6f\x6e\x27" \
b"\x74\x20\x6c\x6f\x61\x64\x20\x73\x79\x73\x74\x65\x6d\x20\x61\x74" \
b"\x74\x72\x69\x62\x75\x74\x65\x73\x20\x2a\x2f\x0d\x0a\x20\x20\x4e" \
b"\x4f\x54\x20\x61\x74\x74\x69\x73\x64\x72\x6f\x70\x70\x65\x64\x0d" \
b"\x0a\x4f\x52\x44\x45\x52\x20\x42\x59\x20\x74\x79\x70\x2e\x6f\x69" \
b"\x64\x2c\x20\x61\x74\x74\x2e\x61\x74\x74\x6e\x75\x6d\x00\x00\x00" \
b"\x42\x00\x00\x00\x0e\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x44" \
b"\x00\x00\x00\x06\x50\x00\x45\x00\x00\x00\x09\x00\x00\x00\x00\x00" \
b"\x50\x00\x00\x00\x93\x00\x2f\x2a\x2a\x2a\x20\x4c\x6f\x61\x64\x20" \
b"\x65\x6e\x75\x6d\x20\x66\x69\x65\x6c\x64\x73\x20\x2a\x2a\x2a\x2f" \
b"\x0d\x0a\x53\x45\x4c\x45\x43\x54\x20\x70\x67\x5f\x74\x79\x70\x65" \
b"\x2e\x6f\x69\x64\x2c\x20\x65\x6e\x75\x6d\x6c\x61\x62\x65\x6c\x0d" \
b"\x0a\x46\x52\x4f\x4d\x20\x70\x67\x5f\x65\x6e\x75\x6d\x0d\x0a\x4a" \
b"\x4f\x49\x4e\x20\x70\x67\x5f\x74\x79\x70\x65\x20\x4f\x4e\x20\x70" \
b"\x67\x5f\x74\x79\x70\x65\x2e\x6f\x69\x64\x3d\x65\x6e\x75\x6d\x74" \
b"\x79\x70\x69\x64\x0d\x0a\x4f\x52\x44\x45\x52\x20\x42\x59\x20\x6f" \
b"\x69\x64\x2c\x20\x65\x6e\x75\x6d\x73\x6f\x72\x74\x6f\x72\x64\x65" \
b"\x72\x00\x00\x00\x42\x00\x00\x00\x0e\x00\x00\x00\x00\x00\x00\x00" \
b"\x01\x00\x00\x44\x00\x00\x00\x06\x50\x00\x45\x00\x00\x00\x09\x00" \
b"\x00\x00\x00\x00\x53\x00\x00\x00\x04"

"""
Contains three queries :
1. 
    /*** Load all supported types ***/
    SELECT ns.nspname, a.typname, a.oid, a.typrelid, a.typbasetype,
    CASE WHEN pg_proc.proname='array_recv' THEN 'a' ELSE a.typtype END AS type,
    CASE
    WHEN pg_proc.proname='array_recv' THEN a.typelem
    WHEN a.typtype='r' THEN rngsubtype
    ELSE 0
    END AS elemoid,
    CASE
    WHEN pg_proc.proname IN ('array_recv','oidvectorrecv') THEN 3    /* Arrays last */
    WHEN a.typtype='r' THEN 2                                        /* Ranges before */
    WHEN a.typtype='d' THEN 1                                        /* Domains before */
    ELSE 0                                                           /* Base types first */
    END AS ord
    FROM pg_type AS a
    JOIN pg_namespace AS ns ON (ns.oid = a.typnamespace)
    JOIN pg_proc ON pg_proc.oid = a.typreceive
    LEFT OUTER JOIN pg_class AS cls ON (cls.oid = a.typrelid)
    LEFT OUTER JOIN pg_type AS b ON (b.oid = a.typelem)
    LEFT OUTER JOIN pg_class AS elemcls ON (elemcls.oid = b.typrelid)
    LEFT OUTER JOIN pg_range ON (pg_range.rngtypid = a.oid) 
    WHERE
    a.typtype IN ('b', 'r', 'e', 'd') OR         /* Base, range, enum, domain */
    (a.typtype = 'c' AND cls.relkind='c') OR /* User-defined free-standing composites (not table composites) by default */
    (pg_proc.proname='array_recv' AND (
        b.typtype IN ('b', 'r', 'e', 'd') OR       /* Array of base, range, enum, domain */
        (b.typtype = 'p' AND b.typname IN ('record', 'void')) OR /* Arrays of special supported pseudo-types */
        (b.typtype = 'c' AND elemcls.relkind='c')  /* Array of user-defined free-standing composites (not table composites) */
    )) OR
    (a.typtype = 'p' AND a.typname IN ('record', 'void'))  /* Some special supported pseudo-types */
    ORDER BY ord

2. 
    /*** Load field definitions for (free-standing) composite types ***/
    SELECT typ.oid, att.attname, att.atttypid
    FROM pg_type AS typ
    JOIN pg_namespace AS ns ON (ns.oid = typ.typnamespace)
    JOIN pg_class AS cls ON (cls.oid = typ.typrelid)
    JOIN pg_attribute AS att ON (att.attrelid = typ.typrelid)
    WHERE
    (typ.typtype = 'c' AND cls.relkind='c') AND
    attnum > 0 AND     /* Don't load system attributes */
    NOT attisdropped
    ORDER BY typ.oid, att.attnum

3. 
    /*** Load enum fields ***/
    SELECT pg_type.oid, enumlabel
    FROM pg_enum
    JOIN pg_type ON pg_type.oid=enumtypid
    ORDER BY oid, enumsortorder

"""

# PBI_MSGS = [PBI_STARTUP_MSG_1, PBI_PASSWORD_MSG_2, PBI_PBDES_MSG_3]
PBI_MSGS = [PBI_STARTUP_MSG_1, PBI_PASSWORD_MSG_2, PBI_PBDE_x3_S]

# psql sequence of messages
PSQL_STARTUP_MSG_1 = b'\x00\x00\x00W\x00\x03\x00\x00user\x00postgres\x00database\x00postgres\x00application_name\x00psql\x00client_encoding\x00WIN1252\x00\x00'
PSQL_PASSWD_MSG_2= b'p\x00\x00\x00(md529c7bf08e60cbef8e4d36c5abc01f638\x00'
PSQL_SIMPLE_QUERY_MSG_3 = b'Q\x00\x00\x00\x19select * from test1;\x00'
PSQL_MSGS = [PSQL_STARTUP_MSG_1, PSQL_PASSWD_MSG_2, PSQL_SIMPLE_QUERY_MSG_3]

def run_UT(host, port, msgs):
    RX_BUFF_SIZE = 4096

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))

        for msg in msgs :
            print("[+] Sending : {}".format(str(msg)))

            sock.sendall(msg)

            response = sock.recv(RX_BUFF_SIZE)

            if not response:
                print("[-] Not Received")
                break

            print("[+] Received {}".format(str(response)))

if __name__ == "__main__" :
    PG_PORT = 5432
    HOST = "localhost"
    #client_msgs = PSQL_MSGS
    client_msgs = PBI_MSGS

    run_UT(HOST, PG_PORT, client_msgs)