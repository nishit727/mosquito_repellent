# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class Mosquito(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, device_id: str=None, specie: int=None):  # noqa: E501
        """Mosquito - a model defined in Swagger

        :param device_id: The device_id of this Mosquito.  # noqa: E501
        :type device_id: str
        :param specie: The specie of this Mosquito.  # noqa: E501
        :type specie: int
        """
        self.swagger_types = {
            'device_id': str,
            'specie': int
        }

        self.attribute_map = {
            'device_id': 'device_id',
            'specie': 'specie'
        }

        self._device_id = device_id
        self._specie = specie

    @classmethod
    def from_dict(cls, dikt) -> 'Mosquito':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Mosquito of this Mosquito.  # noqa: E501
        :rtype: Mosquito
        """
        return util.deserialize_model(dikt, cls)

    @property
    def device_id(self) -> str:
        """Gets the device_id of this Mosquito.


        :return: The device_id of this Mosquito.
        :rtype: str
        """
        return self._device_id

    @device_id.setter
    def device_id(self, device_id: str):
        """Sets the device_id of this Mosquito.


        :param device_id: The device_id of this Mosquito.
        :type device_id: str
        """

        self._device_id = device_id

    @property
    def specie(self) -> int:
        """Gets the specie of this Mosquito.


        :return: The specie of this Mosquito.
        :rtype: int
        """
        return self._specie

    @specie.setter
    def specie(self, specie: int):
        """Sets the specie of this Mosquito.


        :param specie: The specie of this Mosquito.
        :type specie: int
        """

        self._specie = specie
