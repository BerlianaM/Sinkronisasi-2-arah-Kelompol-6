#!C:\Users\PanjiSantoso20\PycharmProjects\MODUL2PraktikumIMS\venv\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'helga==1.7.13','console_scripts','helga'
__requires__ = 'helga==1.7.13'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('helga==1.7.13', 'console_scripts', 'helga')()
    )
