"""Files to ignore"""

import os
from models import db_name

# files in this list will not be tracked in the catalog
ignored = ['catalog.py',
           os.path.basename(__file__),
           db_name
        ]