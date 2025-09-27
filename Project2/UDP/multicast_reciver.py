import socket
import struct
import argparse
import time
import json

mcast_group = '224.1.1.1'
mcast_port = 5007