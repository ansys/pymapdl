# ©2022, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

from typing import Any, Callable, Optional, Tuple

import grpc

from ansys.mapdl.core.metric import Metric


class ClientInterceptor(grpc.UnaryUnaryClientInterceptor,
                          grpc.UnaryStreamClientInterceptor,
                          grpc.StreamUnaryClientInterceptor,
                          grpc.StreamStreamClientInterceptor):
    def __init__(self, metric):
        self.metric: Metric = metric
    
    def intercept_unary_unary(self, continuation, client_call_details, request):
        self.metric.increment_counter()
        result = continuation(client_call_details, request)
        assert isinstance(
            result,
            grpc.Call), '{} ({}) is not an instance of grpc.Call'.format(
                result, type(result))
        assert isinstance(
            result,
            grpc.Future), '{} ({}) is not an instance of grpc.Future'.format(
                result, type(result))
        return result

    def intercept_unary_stream(self, continuation, client_call_details,
                               request):
        self.metric.increment_counter()
        return continuation(client_call_details, request)

    def intercept_stream_unary(self, continuation, client_call_details,
                               request_iterator):
        self.metric.increment_counter()
        result = continuation(client_call_details, request_iterator)
        assert isinstance(
            result,
            grpc.Call), '{} is not an instance of grpc.Call'.format(result)
        assert isinstance(
            result,
            grpc.Future), '{} is not an instance of grpc.Future'.format(result)
        return result

    def intercept_stream_stream(self, continuation, client_call_details,
                                request_iterator):
        self.metric.increment_counter()
        return continuation(client_call_details, request_iterator)