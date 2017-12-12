# Standard library imports
import contextlib

# Third party imports
import pytest

# Local imports
from uplink.clients import (
    AiohttpClient, interfaces, requests_, twisted_, get_client
)

try:
    from uplink.clients import aiohttp_
except SyntaxError:
    aiohttp_ = None


requires_aiohttp = pytest.mark.skipif(
    not aiohttp_, reason="Requires Python 3.4 or above")


@contextlib.contextmanager
def _patch(obj, attr, value):
    if obj is not None:
        old_value = getattr(obj, attr)
        setattr(obj, attr, value)
    yield
    if obj is not None:
        setattr(obj, attr, old_value)


def test_get_client_with_http_client_adapter_subclass():
    class HttpClientAdapterMock(interfaces.HttpClientAdapter):
        def create_request(self):
            pass

    client = get_client(HttpClientAdapterMock)
    assert isinstance(client, HttpClientAdapterMock)


class TestRequests(object):

    def test_get_client(self, mocker):
        import requests
        session_mock = mocker.Mock(spec=requests.Session)
        client = get_client(session_mock)
        assert isinstance(client, requests_.RequestsClient)


class TestTwisted(object):

    def test_init_without_client(self):
        twisted = twisted_.TwistedClient()
        assert isinstance(twisted._requests, requests_.RequestsClient)

    def test_create_requests(self, http_client_mock):
        twisted = twisted_.TwistedClient(http_client_mock)
        request = twisted.create_request()
        assert request._proxy is http_client_mock.create_request()
        assert isinstance(request, twisted_.Request)

    def test_create_requests_no_twisted(self, http_client_mock):
        with _patch(twisted_, "threads", None):
            with pytest.raises(NotImplementedError):
                twisted_.TwistedClient(http_client_mock)

    def test_request_send(self, mocker,  request_mock):
        deferToThread = mocker.patch.object(twisted_.threads, "deferToThread")
        request = twisted_.Request(request_mock)
        request.send(1, 2, 3)
        deferToThread.assert_called_with(request_mock.send, 1, 2, 3)

    def test_request_send_with_callback(self, mocker, request_mock):
        # Setup
        callback = mocker.stub()
        deferred = mocker.Mock()
        deferToThread = mocker.patch.object(twisted_.threads, "deferToThread")
        deferToThread.return_value = deferred
        request = twisted_.Request(request_mock)
        request.add_callback(callback)

        # Run
        request.send(1, 2, 3)

        # Verify
        deferred.addCallback.assert_called_with(callback)
        deferToThread.assert_called_with(request_mock.send, 1, 2, 3)


@pytest.fixture
def aiohttp_session_mock(mocker):
    import aiohttp
    return mocker.Mock(spec=aiohttp.ClientSession)


class TestAiohttp(object):

    def test_init_when_aiohttp_is_not_installed(self):
        with _patch(aiohttp_, "aiohttp", None):
            with pytest.raises(NotImplementedError):
                AiohttpClient()

    @requires_aiohttp
    def test_get_client(self, aiohttp_session_mock):
        client = get_client(aiohttp_session_mock)
        assert isinstance(client, aiohttp_.AiohttpClient)

    @requires_aiohttp
    def test_create_request(self, aiohttp_session_mock):
        aiohttp = aiohttp_.AiohttpClient(aiohttp_session_mock)
        assert isinstance(aiohttp.create_request(), aiohttp_.Request)

    @requires_aiohttp
    def test_request_send(self, aiohttp_session_mock):
        # Setup
        import asyncio

        @asyncio.coroutine
        def request(*args, **kwargs):
            return 0

        aiohttp_session_mock.request = request
        client = aiohttp_.AiohttpClient(aiohttp_session_mock)
        request = aiohttp_.Request(client)

        # Run
        response = request.send(1, 2, {})
        loop = asyncio.get_event_loop()
        value = loop.run_until_complete(asyncio.ensure_future(response))

        # Verify
        assert value == 0

    @requires_aiohttp
    def test_callback(self, aiohttp_session_mock):
        # Setup
        import asyncio

        @asyncio.coroutine
        def request(*args, **kwargs):
            return 2

        aiohttp_session_mock.request = request
        client = aiohttp_.AiohttpClient(aiohttp_session_mock, asyncio.coroutine)
        request = aiohttp_.Request(client)

        # Run
        request.add_callback(lambda x: 2)
        response = request.send(1, 2, {})
        loop = asyncio.get_event_loop()
        value = loop.run_until_complete(asyncio.ensure_future(response))

        # Verify
        assert value == 2

    @requires_aiohttp
    def test_threaded_callback(self, mocker):
        import asyncio

        def callback(response):
            return response

        # Mock response.
        response = mocker.Mock()
        response.text = asyncio.coroutine(mocker.stub())

        # Run
        new_callback = aiohttp_.threaded_callback(callback)
        return_value = new_callback(response)
        loop = asyncio.get_event_loop()
        value = loop.run_until_complete(asyncio.ensure_future(return_value))

        # Verify
        response.text.assert_called_with()
        assert value == response

    @requires_aiohttp
    def test_threaded_coroutine(self):
        # Setup
        import asyncio

        @asyncio.coroutine
        def coroutine():
            return 1

        threaded_coroutine = aiohttp_.ThreadedCoroutine(coroutine)

        # Run -- should block
        response = threaded_coroutine()

        # Verify
        assert response == 1

    @requires_aiohttp
    def test_threaded_response(self, mocker):
        # Setup
        import asyncio

        @asyncio.coroutine
        def coroutine():
            return 1

        response = mocker.Mock()
        response.text = coroutine
        threaded_response = aiohttp_.ThreadedResponse(response)

        # Run
        threaded_coroutine = threaded_response.text
        return_value = threaded_coroutine()

        # Verify
        assert isinstance(threaded_coroutine, aiohttp_.ThreadedCoroutine)
        assert return_value == 1

    @requires_aiohttp
    def test_create(self, mocker):
        # Setup
        import asyncio

        session_cls_mock = mocker.patch("aiohttp.ClientSession")
        positionals = [1]
        keywords = {"keyword": 2}

        # Run: Create client
        client = aiohttp_.AiohttpClient.create(*positionals, **keywords)

        # Verify: session hasn't been created yet.
        assert not session_cls_mock.called

        # Run: Get session
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.ensure_future(client.session()))

        # Verify: session created with args
        session_cls_mock.assert_called_with(*positionals, **keywords)
