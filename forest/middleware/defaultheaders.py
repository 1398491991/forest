#coding=utf-8

class DefaultHeadersMiddleware(object):

    def process_request(self,request):
        # assert isinstance(request,dict)
        request.setdefault('headers',{'user-agent':'forest'})
        return request

    @classmethod
    def from_settings(cls,settings):
        pass
