from handler import *
from settings import host_exp, api_host_exp, self_exp

urls = [
    (r'/register/', RegisterHandler, self_exp),
    (r'/login/', LoginHandler, self_exp),
    (r'/reapply/', ReapplyHandler, self_exp),
    (r'/change/', ChangeHandler, self_exp),

    (r'/info/', InfoHandler, self_exp),
    (r'/info/routes/', InfoRoutesHandler, self_exp),
    (r'/info/(?P<hid>\d+)/detail/', HttpLogDetailHandler, self_exp),
    (r'/list/(?P<page>\d+)/(?P<size>\d+)/', RequestListHandler, self_exp),

    (r'/search/ct/', SearchCTHandler, self_exp),
    (r'/search/ip/', SearchIPHandler, self_exp),

    (r'/download/', DownloadHandler, self_exp),
    (r'/download/all/', DownloadAllHandler, self_exp),
    (r'/delete/', DeleteHandler, self_exp),
    (r'/delete/all/', DeleteAllHandler, self_exp),

    (r'/route/(?P<rid>\d+)/', RouteHandler, self_exp),
    (r'/route/add/', RouteAddHandler, self_exp),
    (r'/file/(?P<hash>[0-9a-f]+)/download/', FileDownloadHandler, self_exp),

    (r'/', HTMLHandler, self_exp),
    
    (r'.*', ReceiveHandler, host_exp)
]