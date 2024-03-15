from instagrapi import Client

import os
import requests
import base64
from getpass import getpass
from datetime import datetime, timedelta, timezone

class Client(object):
    def __init__(self) -> None:
        self.ig = Client()
        

