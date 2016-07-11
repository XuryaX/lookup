#!/bin/bash

virtualenv lookupPython
. lookupPython/bin/activate
pip install -r Lookup/requirements.txt
deactivate
echo "#!/bin/bash" >> run.sh
echo ". lookupPython/bin/activate" >> run.sh
echo "python Lookup/Run.py" >> run.sh
rm install.sh