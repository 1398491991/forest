#coding=utf-8

class DefaultHeadersMiddleware(object):
    def __init__(self,settings):
        self.settings=settings

    def process_request(self,request):
        # assert isinstance(request,dict)
        request.setdefault('headers',self.settings.get('default_headers',
                                                       {'user-agent':'forest'}
                                                       )
                           )
        return request

    @classmethod
    def from_settings(cls,settings):
        return cls(settings)
