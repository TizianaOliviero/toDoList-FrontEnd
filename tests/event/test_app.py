from unittest.mock import Mock, patch, mock_open

from event.app import App, main


def mock_response_dict(status_code, data={}):
    res = Mock()
    res.status_code = status_code
    res.json.return_value = data
    return res


def mock_response(status_code, data=[]):
    res = Mock()
    res.status_code = status_code
    res.json.return_value = data
    return res


@patch('builtins.input', side_effect=['0'])
@patch('builtins.print')
def test_exit(mocked_print, mocked_input):
    with patch('builtins.open'):
        App().run()
    mocked_print.assert_any_call('*** To Do List Login ***')
    mocked_print.assert_any_call('0:\tExit')
    mocked_print.assert_any_call('Bye!')
    mocked_input.assert_called()

@patch('requests.post', side_effect=[mock_response_dict(400)])
@patch('requests.get', side_effect=[mock_response_dict(403)])
@patch('builtins.input', side_effect=['1', 'supevvfrptnmd', '0;gs4ssQR<','0'])
@patch('builtins.print')
def test_wrong_credentials(mocked_print, mocked_input, mocked_requests_get, mocked_requests_post):
    with patch('builtins.open'):
        App().run()
    mocked_print.assert_any_call('*** To Do List Login ***')
    mocked_requests_post.assert_called()
    mocked_input.assert_called()
    mocked_print.assert_any_call('Wrong Credentials!')


@patch('requests.post', side_effect=[mock_response_dict(200, {'key': '301ed42f7db4a71b682716f7b3e351a2dd10c459'})])
@patch('requests.get', side_effect=[mock_response(200, [{'id': 1,
                                                         'name': 'Calcetto',
                                                         'description': '11 vs 11',
                                                         'author': 1,
                                                         'start_date': '2021-12-25T12:12:12Z',
                                                         'end_date': '2021-12-26T12:12:12Z',
                                                         'location': 'stadio',
                                                         'category': 1,
                                                         'priority': 1},
                                                        ])])
@patch('builtins.input', side_effect=['1', 'superptnmd', '0;gs4QR<!', '5','0','0'])
@patch('builtins.print')
def test_fetch(mocked_print, mocked_input, mocked_requests_get, mocked_requests_post):
    with patch('builtins.open'):
        App().run()
    mocked_requests_post.assert_called()
    mocked_requests_get.assert_called()
    mocked_print.assert_any_call('*** To Do List Home ***')
