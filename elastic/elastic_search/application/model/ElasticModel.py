import re
import logging
import os
from dataclasses import dataclass


@dataclass
class ElasticModel:
    query: str


