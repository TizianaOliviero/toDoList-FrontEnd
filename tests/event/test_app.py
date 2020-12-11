from unittest.mock import Mock, patch, mock_open

from event.app import App, main


def mock_response_dict(status_code, data={}):
    res = Mock()
    res.status_code = status_code
    res.json.return_value = data
    return res


def mock_response(status_code, data={}):
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

@patch('requests.post', side_effect=[mock_response_dict(400)])
@patch('requests.get', side_effect=[mock_response_dict(403)])
@patch('builtins.input', side_effect=['2', 'tiziana2', 'qq@example.it', 'w34R...---', 'w34R...---','0'])
@patch('builtins.print')
def test_register_user_already_exists(mocked_print, mocked_input, mocked_requests_get, mocked_requests_post):
    with patch('builtins.open'):
        App().run()
    mocked_requests_post.assert_called()
    mocked_input.assert_called()
    mocked_print.assert_any_call('Something went wrong')

@patch('requests.post', side_effect=[mock_response_dict(400)])
@patch('requests.get', side_effect=[mock_response_dict(403)])
@patch('builtins.input', side_effect=['2', 'tiziana2', 'qq@example.it', 'qwerty', 'qwerty','0'])
@patch('builtins.print')
def test_register_user_common_password(mocked_print, mocked_input, mocked_requests_get, mocked_requests_post):
    with patch('builtins.open'):
        App().run()
    mocked_requests_post.assert_called()
    mocked_input.assert_called()
    mocked_print.assert_any_call('Something went wrong')

@patch('requests.post', side_effect=[mock_response_dict(200, {'key': '301ed42f7db4a71b682716f7b3e351a2dd10c459'}),
                                     mock_response_dict(200)])
@patch('requests.get', side_effect=[mock_response(200, {'id': 1}),
                                    mock_response(200, [{'id': 1,
                                                         'name': 'Calcetto',
                                                         'description': '11 vs 11',
                                                         'author': 1,
                                                         'start_date': '2021-12-25T12:12:12Z',
                                                         'end_date': '2021-12-26T12:12:12Z',
                                                         'location': 'stadio',
                                                         'category': 1,
                                                         'priority': 1},
                                                        ])])
@patch('builtins.input', side_effect=['1', 'superptnmd', '0;gs4QR<!','0','0'])
@patch('builtins.print')
def test_fetch(mocked_print, mocked_input, mocked_requests_get, mocked_requests_post):
    with patch('builtins.open'):
        App().run()
    mocked_requests_post.assert_called()
    mocked_input.assert_called()
    mocked_requests_get.assert_called_with(url='http://localhost:8000/api/v1/events', headers={'Authorization': 'Token 301ed42f7db4a71b682716f7b3e351a2dd10c459'})
    mocked_print.assert_any_call('Logged out!')


@patch('requests.post', side_effect=[mock_response_dict(200, {'key': '301ed42f7db4a71b682716f7b3e351a2dd10c459'}),
                                     mock_response_dict(200),
                                     mock_response_dict(200),])
@patch('requests.get', side_effect=[mock_response_dict(200, {'id': 1}),
                                    mock_response_dict(400),
                                    mock_response_dict(400)])
@patch('builtins.input', side_effect=['1', 'tiziana2', 'w34R...---', '1', 'evento1', 'desc', '1/1/22T12:12:12Z',
                                      '1/1/22T12:12:12Z', 'location', '1','1','0','0'])
@patch('builtins.print')
def test_add_event(mocked_print, mocked_input, mocked_requests_get, mocked_requests_post):
    with patch('builtins.open'):
        App().run()
    mocked_requests_post.assert_called()
    mocked_input.assert_called()
    mocked_print.assert_any_call('Event added!')


@patch('requests.post', side_effect=[mock_response_dict(200, {'key': '301ed42f7db4a71b682716f7b3e351a2dd10c459'}),
                                     mock_response_dict(200)])
@patch('requests.get', side_effect=[mock_response_dict(200, {'id': 1}),
                                    mock_response(200, [{'id': 1,
                                                         'name': 'Calcetto',
                                                         'description': '11 vs 11',
                                                         'author': 1,
                                                         'start_date': '2021-12-25T12:12:12Z',
                                                         'end_date': '2021-12-26T12:12:12Z',
                                                         'location': 'stadio',
                                                         'category': 1,
                                                         'priority': 1},
                                                        ])])
@patch('requests.delete', side_effect=[mock_response(200)])
@patch('builtins.input', side_effect=['1', 'tiziana2', 'w34R...---', '2', '1','0','0'])
@patch('builtins.print')
def test_remove_event(mocked_print, mocked_input, mocked_requests_get, mocked_requests_post, mocked_requests_delete):
    with patch('builtins.open'):
        App().run()
    mocked_requests_post.assert_called()
    mocked_input.assert_called()
    mocked_requests_delete.assert_called()
    mocked_print.assert_any_call('Event removed')