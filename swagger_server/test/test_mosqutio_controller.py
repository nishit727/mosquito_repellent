# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.daterange import Daterange  # noqa: E501
from swagger_server.models.mosquito import Mosquito  # noqa: E501
from swagger_server.test import BaseTestCase


class TestMosqutioController(BaseTestCase):
    """MosqutioController integration test stubs"""

    def test_add_mosqutio(self):
        """Test case for add_mosqutio

        Add a detected mosquito
        """
        mosquito = Mosquito()
        response = self.client.open(
            '/mosquito_repellent/mosqutio/store',
            method='POST',
            data=json.dumps(mosquito),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_mosqutio(self):
        """Test case for get_mosqutio

        Get detected mosqutio data in given time frame
        """
        daterange = Daterange()
        response = self.client.open(
            '/mosquito_repellent/mosqutio/retive',
            method='GET',
            data=json.dumps(daterange),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
