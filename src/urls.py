from handler import *
from settings import host_exp, api_host_exp, self_exp

urls = [
    (r'/register/', RegisterHandler, api_host_exp),
    (r'/login/', LoginHandler, api_host_exp),
    (r'/reapply/', ReapplyHandler, api_host_exp),
    (r'/change/', ChangeHandler, api_host_exp),

    (r'/info/', InfoHandler, api_host_exp),
    (r'/info/routes/', InfoRoutesHandler, api_host_exp),
    (r'/info/(?P<hid>\d+)/detail/', HttpLogDetailHandler, api_host_exp),
    (r'/list/(?P<page>\d+)/(?P<size>\d+)/', RequestListHandler, api_host_exp),

    (r'/search/ct/', SearchCTHandler, api_host_exp),
    (r'/search/ip/', SearchIPHandler, api_host_exp),

    (r'/download/', DownloadHandler, api_host_exp),
    (r'/download/all/', DownloadAllHandler, api_host_exp),
    (r'/delete/', DeleteHandler, api_host_exp),
    (r'/delete/all/', DeleteAllHandler, api_host_exp),

    (r'/route/(?P<rid>\d+)/', RouteHandler, api_host_exp),
    (r'/route/add/', RouteAddHandler, api_host_exp),
    (r'/file/(?P<hash>[0-9a-f]+)/download/', FileDownloadHandler, api_host_exp),

    (r'/', HTMLHandler, self_exp),
    
    (r'.*', ReceiveHandler, host_exp)
]