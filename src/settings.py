import os
import base64
from pathlib import Path


BASE_DIR = Path(__file__).resolve(strict=True).parent

SECRET_KEY = 'VBJKL:"?>}{POIR$%^&*$#EDFGNML:"}"{POIUGVB'

host = 'httpbin.icu'

settings = dict(
    static_path = os.path.join(BASE_DIR, 'dist', 'static'),
    static_url_prefix = '/static/'
)

host_exp = r'^.+\.' + host.replace(".", "\\.") + r'$'  # 绑定泛域名正则表达式
api_host_exp = r'^api\.' + host.replace(".", "\\.") + r'$'
self_exp = host.replace(".", "\\.") + r'$'

# TODO: IP mode
ip_exp = r'^\d+\.\d+\.\d+\.\d+$'

salt = b'p9_}8#6&^_1%8{s:^l{}h*bf}?9|?"!1'