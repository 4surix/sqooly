# encode: utf-8
# Python 3.10.12
# ----------------------------------------------------------------------------

import os
import sqooly


globals().update(sqooly.database.create(os.path.dirname(__file__)).commands)