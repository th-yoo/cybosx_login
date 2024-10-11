import os, sys
import logging
import win32api
import win32con

from cred_retrieve import create_provider
from run_as_task import run_as_task

try:
    from cybosx_login import login, logger
    print('from installed package')
except:
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    sys.path.append(parent_dir)
    from cybosx_login import login, logger
    print('from source')

#
# logging stuff
#
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
file_handler = logging.FileHandler('cybosx.log')

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)

def main():
    run_as_task()

    logger.debug('Start')

    # get KeePassXC passphrase
    try:
        cred_env = create_provider('dotenv')
    except Exception as e:
        logger.error(e)
        raise e

    db = os.path.join(os.getenv('PROGRAMDATA'), 'KeePassXC', 'trading_password.kdbx')

    # get credential from KeePassXC
    try:
        cred_kpx = create_provider('keepassxc', db)
    except Exception as e:
        logger.error(e)
        raise e

    # login cybosplus 
    try:
        login(*cred_kpx.get_id_pw(cred_env['PW'], 'daishin'))
    except Exception as e:
        logger.error(e)
        raise e

    logger.debug('Finished!')
    if 'pythonw' in os.path.basename(sys.executable):
        win32api.MessageBox(0, 'Finished!', 'test', win32con.MB_OK)

if __name__ == '__main__':
    main()
