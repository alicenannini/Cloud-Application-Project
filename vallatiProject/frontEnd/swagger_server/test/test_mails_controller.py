# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.mail import Mail  # noqa: E501
from swagger_server.test import BaseTestCase


class TestMailsController(BaseTestCase):
    """MailsController integration test stubs"""

    def test_addmail(self):
        """Test case for addmail

        Add a new mail
        """
        body = Mail()
        response = self.client.open(
            '/mail/mails',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_deletemail(self):
        """Test case for deletemail

        Deletes an mail
        """
        response = self.client.open(
            '/mail/mails/{mailId}'.format(mailId=789),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_getmail_by_id(self):
        """Test case for getmail_by_id

        Find mail by ID
        """
        response = self.client.open(
            '/mail/mails/{mailId}'.format(mailId=789),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_updatemail(self):
        """Test case for updatemail

        Update an existing mail
        """
        body = Mail()
        response = self.client.open(
            '/mail/mails',
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_updatemail_with_form(self):
        """Test case for updatemail_with_form

        Updates an mail in the store with form data
        """
        data = dict(name='name_example',
                    status='status_example')
        response = self.client.open(
            '/mail/mails/{mailId}'.format(mailId=789),
            method='POST',
            data=data,
            content_type='application/x-www-form-urlencoded')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
