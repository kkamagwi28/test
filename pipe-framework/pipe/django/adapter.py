from pipe.server.pipe import HTTPPipe
from django.http.response import HttpResponseBase, HttpResponse
from django.views import View


class DjangoHttpPipe(HTTPPipe):
    def interrupt(self, store) -> bool:
        return issubclass(store.__class__, HttpResponseBase) or isinstance(store, HttpResponse)


class PipeView(View):
    pipe: DjangoHttpPipe

    def get_pipe_object(self, request):
        if not issubclass(self.pipe, DjangoHttpPipe):
            raise Exception('pipe property should be a subclass of DjangoHttpPipe')

        return self.pipe(request, {})

    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() in self.http_method_names:
            pipe_obj = self.get_pipe_object(request)
            result = pipe_obj.run_pipe()
        else:
            return self.http_method_not_allowed(request, *args, **kwargs)

        return result
