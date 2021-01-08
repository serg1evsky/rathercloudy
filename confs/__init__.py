import os
import ast
from .crypt import LetItCrypt
from vk_api import VkApi
from Crypto.Cipher import DES

SYNC_CODE = "Archive: RatherCloudy"
PEER_CONST = 2000000000

class Config(object):

    __slots__ = ('crypter','data')

    def __init__(self,passw):
        self.crypter = LetItCrypt(passw)
        if not os.path.exists('data'):
            self.new_cfg()
        config_as_str = self.crypter.dec()
        self.data = ast.literal_eval(config_as_str)
    
    def get_archive_title(self,id: int, api_methods: VkApi) -> str:
        return api_methods.messages.getChat(chat_id = id - PEER_CONST)['title']

    def get_all_archives(self,token: str) -> list:
        session = VkApi(token=token)
        api = session.get_api()
        messages = api.messages.search(q=SYNC_CODE,count=100)
        all_archives = []
        if messages:
            for d in messages['items']:
                if d['peer_id'] > PEER_CONST:
                    archive_title = self.get_archive_title(d['peer_id'], api)
                    all_archives.append({'name': archive_title,'id':d['peer_id']})
        return all_archives

    def new_cfg(self):
        token = input('Введите токен для vk_api (kate mobile token): ')
        archives = self.get_all_archives(token)
        new_config = {
            'token': token, 
            'sync_chat':None,
            'archives': archives,
        }
        self.crypter.enc(str(new_config))
    
    def save_in_file(self) -> None:
        self.crypter.enc(str(self.data))
        config_as_str = self.crypter.dec()
        self.data = ast.literal_eval(config_as_str)