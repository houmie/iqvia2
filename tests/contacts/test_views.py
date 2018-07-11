from .. import post, get, delete
from iqvia.contacts.models import Contact, Email
from unittest.mock import Mock


def test_add_contact_ok(monkeypatch):
    """
    Testing a valid contact creation.
    :param monkeypatch: a monkeypatching instance.
    :return:
    """
    test_data = {"first_name": "tesfirstname",
                 "surname": "testsurname",
                 "emails": [{"email": "testemail1@gmail.com"},
                            {"email": "testemail2@gmail.com"}],
                 "username": "testusername1234"}

    database_mock = Mock()

    monkeypatch.setattr('iqvia.contacts.views.uuid4', Mock(return_value='7e8377af-bdc3-4b9e-a491-2d9ddff3253f'))
    monkeypatch.setattr('iqvia.contacts.views.db.session.add', database_mock)
    monkeypatch.setattr('iqvia.contacts.views.db.session.flush', database_mock)
    monkeypatch.setattr('iqvia.contacts.views.does_contact_username_exist', Mock(return_value=False))
    status_code, response_data = post('contacts/', test_data)
    assert response_data == {'surname': 'testsurname',
                             'first_name': 'tesfirstname',
                             'id': '7e8377af-bdc3-4b9e-a491-2d9ddff3253f',
                             'username': 'testusername1234',
                             'emails': [{'email': 'testemail1@gmail.com'}, {'email': 'testemail2@gmail.com'}]}
    assert status_code == 200
    assert database_mock.call_count == 2


def test_add_contact_nok_username_already_exists(monkeypatch):
    """
    Testing an invalid contact creation: the username already exists
    :return:
    """
    test_data = {"first_name": "tesfirstname",
                 "surname": "testsurname",
                 "emails": [{"email": "testemail1@gmail.com"},
                            {"email": "testemail2@gmail.com"}],
                 "username": "testusername1234"}
    database_mock = Mock()
    monkeypatch.setattr('iqvia.contacts.views.uuid4', Mock(return_value='7e8377af-bdc3-4b9e-a491-2d9ddff3253f'))
    monkeypatch.setattr('iqvia.contacts.views.db.session.add', database_mock)
    monkeypatch.setattr('iqvia.contacts.views.db.session.commit', database_mock)
    monkeypatch.setattr('iqvia.contacts.views.does_contact_username_exist', Mock(return_value=True))
    status_code, response_data = post('contacts/', test_data)

    assert response_data == {'errors': [{'message': 'Sorry, the username testusername1234 '
                                                    'of the contact you try to add already exists'}]}
    assert status_code == 400
    assert database_mock.call_count == 0


def test_get_contacts_ok(monkeypatch):
    """
    Testing a valid contact fetching: list of contacts found.
    :param monkeypatch: a monkeypatching instance.
    :return:
    """
    email_11 = Email(email='testemail1@gmail.com')
    email_12 = Email(email='testemail2@gmail.com')

    email_21 = Email(email='testemail3@gmail.com')
    email_22 = Email(email='testemail4@gmail.com')

    contact_1 = Contact(id='7e8377af-bdc3-4b9e-a491-2d9ddff3253f', first_name='testfirstname1',
                        surname='testsurname1', username='testusername1234', emails=[email_11, email_12])
    contact_2 = Contact(id='6e8377af-bdc3-4b9e-a491-2d9ddff3253g', first_name='testfirstname2',
                        surname='testsurname2', username='testusername4567', emails=[email_21, email_22])

    get_mock = Mock(query=Mock(options=Mock(return_value=Mock(all=Mock(return_value=[contact_1, contact_2])))))
    monkeypatch.setattr('iqvia.contacts.views.Contact', get_mock)

    status_code, response_data = get('contacts/')
    assert response_data == {'contacts': [{'id': '7e8377af-bdc3-4b9e-a491-2d9ddff3253f',
                                           'surname': 'testsurname1',
                                           'emails': [{'email': 'testemail1@gmail.com'},
                                                      {'email': 'testemail2@gmail.com'}],
                                           'username': 'testusername1234',
                                           'first_name': 'testfirstname1'},
                                          {'id': '6e8377af-bdc3-4b9e-a491-2d9ddff3253g',
                                           'surname': 'testsurname2',
                                           'emails': [{'email': 'testemail3@gmail.com'},
                                                      {'email': 'testemail4@gmail.com'}],
                                           'username': 'testusername4567',
                                           'first_name': 'testfirstname2'}]}
    assert status_code == 200


def test_get_contact_by_username_ok(monkeypatch):
    """
    Testing a valid get by username scenario.
    :param monkeypatch: a monkeypatching instance.
    :return:
    """
    email = Email(email='testemail1@gmail.com')
    contact = Contact(id='7e8377af-bdc3-4b9e-a491-2d9ddff3253f', first_name='testfirstname',
                      surname='testsurname', username='testusername1234', emails=[email])

    get_mock = Mock(query=Mock(options=Mock(return_value=Mock(
        filter=Mock(return_value=Mock(first=Mock(return_value=contact)))))))

    monkeypatch.setattr('iqvia.contacts.views.Contact', get_mock)

    status_code, response_data = get('contacts/contact?username=testusername1234')
    assert response_data == {'emails': [{'email': 'testemail1@gmail.com'}],
                             'id': '7e8377af-bdc3-4b9e-a491-2d9ddff3253f',
                             'username': 'testusername1234',
                             'first_name': 'testfirstname',
                             'surname': 'testsurname'}
    assert status_code == 200


def test_get_contact_by_email_ok(monkeypatch):
    """
    Testing a valid get by email scenario.
    :param monkeypatch: a monkeypatching instance.
    :return:
    """
    email = Email(email='testemail1@gmail.com')
    contact = Contact(id='7e8377af-bdc3-4b9e-a491-2d9ddff3253f', first_name='testfirstname',
                      surname='testsurname', username='testusername1234', emails=[email])

    get_mock = Mock(query=Mock(options=Mock(return_value=Mock(
        filter=Mock(return_value=Mock(first=Mock(return_value=contact)))))))

    monkeypatch.setattr('iqvia.contacts.views.Contact', get_mock)

    status_code, response_data = get('contacts/contact?email=testemail1@gmail.com')

    assert response_data == {'emails': [{'email': 'testemail1@gmail.com'}],
                             'id': '7e8377af-bdc3-4b9e-a491-2d9ddff3253f',
                             'username': 'testusername1234',
                             'first_name': 'testfirstname',
                             'surname': 'testsurname'}
    assert status_code == 200


def test_delete_contacts_ok(monkeypatch):
    """
    Testing a valid delete scenario.
    :param monkeypatch: a monkeypatching instance.
    :return:
    """
    email = Email(email='testemail1@gmail.com')

    contact = Contact(id='7e8377af-bdc3-4b9e-a491-2d9ddff3253f', first_name='testfirstname',
                      surname='testsurname', username='testusername1234', emails=[email])
    database_mock = Mock()
    monkeypatch.setattr('iqvia.contacts.views.Contact',
                        Mock(query=Mock(filter=Mock(return_value=Mock(first=Mock(return_value=contact))))))
    monkeypatch.setattr('iqvia.contacts.views.db.session.delete', database_mock)
    monkeypatch.setattr('iqvia.contacts.views.db.session.commit', database_mock)

    status_code = delete('contacts/7e8377af-bdc3-4b9e-a491-2d9ddff3253f')

    assert database_mock.call_count == 2
    assert status_code == 204


def test_delete_contacts_nok_contact_not_found(monkeypatch):
    """
    Testing a invalid delete scenario: contact not found.
    :param monkeypatch: a monkeypatching instance.
    :return:
    """
    database_mock = Mock()
    monkeypatch.setattr('iqvia.contacts.views.Contact',
                        Mock(query=Mock(filter=Mock(return_value=Mock(first=Mock(return_value=None))))))
    monkeypatch.setattr('iqvia.contacts.views.db.session.delete', database_mock)
    monkeypatch.setattr('iqvia.contacts.views.db.session.commit', database_mock)
    status_code = delete('contacts/7e8377af-bdc3-4b9e-a491-2d9ddff3253f')
    assert status_code == 400
    assert database_mock.call_count == 0


def test_update_contact_ok(monkeypatch):
    """
    Testing a valid contact update.
    :param monkeypatch: a monkeypatching instance.
    :return:
    """
    email = Email(email='testemail1@gmail.com')
    test_data = {"first_name": "tesfirstnameUPDATED",
                 "surname": "testsurnameUPDATED",
                 "emails": [{"email": "testemail1comUPDATED@gmail.com"}, {"email": "testemail2comUPDATED@gmail.com"}],
                 "username": "testusername1234UPDATED"}

    contact = Contact(id='7e8377af-bdc3-4b9e-a491-2d9ddff3253f', first_name='testfirstname',
                      surname='testsurname', username='testusername1234', emails=[email])
    database_mock = Mock()

    monkeypatch.setattr('iqvia.contacts.views.uuid4', Mock(return_value='7e8377af-bdc3-4b9e-a491-2d9ddff3253f'))
    monkeypatch.setattr('iqvia.contacts.views.db.session.flush', database_mock)
    monkeypatch.setattr('iqvia.contacts.views.does_contact_username_exist', Mock(return_value=False))

    get_mock = Mock(query=Mock(options=Mock(return_value=Mock(
        filter=Mock(return_value=Mock(first=Mock(return_value=contact)))))))

    monkeypatch.setattr('iqvia.contacts.views.Contact', get_mock)
    status_code, response_data = post('contacts/7e8377af-bdc3-4b9e-a491-2d9ddff3253f', test_data)

    assert response_data == {'emails': [{'email': 'testemail1comUPDATED@gmail.com'},
                                        {'email': 'testemail2comUPDATED@gmail.com'}],
                             'first_name': 'tesfirstnameUPDATED',
                             'id': '7e8377af-bdc3-4b9e-a491-2d9ddff3253f',
                             'surname': 'testsurnameUPDATED',
                             'username': 'testusername1234UPDATED'}

    assert status_code == 200
    assert database_mock.call_count == 1


def test_update_contact_nok_username_already_exists(monkeypatch):
    """
    Testing a invalid contact update: the username passed already exists.
    :param monkeypatch: a monkeypatching instance.
    :return:
    """
    email = Email(email='testemail1@gmail.com')
    test_data = {"first_name": "tesfirstnameUPDATED",
                 "surname": "testsurnameUPDATED",
                 "emails": [{"email": "testemail1comUPDATED@gmail.com"}, {"email": "testemail2comUPDATED@gmail.com"}],
                 "username": "testusername1234UPDATED"}

    contact = Contact(id='7e8377af-bdc3-4b9e-a491-2d9ddff3253f', first_name='testfirstname',
                      surname='testsurname', username='testusername1234', emails=[email])
    database_mock = Mock()

    monkeypatch.setattr('iqvia.contacts.views.uuid4', Mock(return_value='7e8377af-bdc3-4b9e-a491-2d9ddff3253f'))
    monkeypatch.setattr('iqvia.contacts.views.db.session.flush', database_mock)
    monkeypatch.setattr('iqvia.contacts.views.does_contact_username_exist', Mock(return_value=True))

    get_mock = Mock(query=Mock(options=Mock(return_value=Mock(
        filter=Mock(return_value=Mock(first=Mock(return_value=contact)))))))

    monkeypatch.setattr('iqvia.contacts.views.Contact', get_mock)
    status_code, response_data = post('contacts/7e8377af-bdc3-4b9e-a491-2d9ddff3253f', test_data)

    assert response_data == {'errors':
                                 [{'message': 'Sorry, you cannot update the contact with the '
                                              'username testusername1234UPDATED: it already exists'}]}
    assert status_code == 400
    assert database_mock.call_count == 0


#
def test_update_contact_nok_contact_not_found(monkeypatch):
    """
    Testing a invalid contact update: the contact is not found.
    :param monkeypatch: a monkeypatching instance.
    :return:
    """
    test_data = {"first_name": "tesfirstnameUPDATED",
                 "surname": "testsurnameUPDATED",
                 "emails": [{"email": "testemail1comUPDATED@gmail.com"}, {"email": "testemail2comUPDATED@gmail.com"}],
                 "username": "testusername1234UPDATED"}
    database_mock = Mock()

    monkeypatch.setattr('iqvia.contacts.views.uuid4', Mock(return_value='7e8377af-bdc3-4b9e-a491-2d9ddff3253f'))
    monkeypatch.setattr('iqvia.contacts.views.db.session.flush', database_mock)
    monkeypatch.setattr('iqvia.contacts.views.does_contact_username_exist', Mock(return_value=True))

    get_mock = Mock(query=Mock(options=Mock(return_value=Mock(
        filter=Mock(return_value=Mock(first=Mock(return_value=None)))))))

    monkeypatch.setattr('iqvia.contacts.views.Contact', get_mock)
    status_code, response_data = post('contacts/7e8377af-bdc3-4b9e-a491-2d9ddff3253f', test_data)

    assert response_data == {'errors':[{'message': 'Sorry, '
                                                   'the contact 7e8377af-bdc3-4b9e-a491-2d9ddff3253f you '
                                                   'try to update does not exist'}]}
    assert status_code == 400
    assert database_mock.call_count == 0
