# IVY is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# IVY is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with IVY.  If not, see <http://www.gnu.org/licenses/>.


"""
Created on Mar 6, 2014

author: jakeret
"""
import pickle

from ivy.context import ctx
from ivy.utils.struct import ImmutableStruct
from ivy.utils.struct import Struct


class DefaultContextProvider:
    """
    Default implementation of a context provider.
    Creates a simple mutable struct as ctx and doesn't
    persist the context.
    """

    @staticmethod
    def create_context(**args):
        """
        Returns a Struct
        """
        return Struct(**args)

    @staticmethod
    def create_immutable_context(**args):
        """
        Returns a Struct
        """
        return ImmutableStruct(**args)

    @staticmethod
    def store_context():
        """
        Dummy method. Nothing is stored
        """
        pass


class PickleContextProvider(DefaultContextProvider):
    """
    Extends the DefaultContextProvider. 
    Persists the context to the disk by using pickle.
    Requires the attribute 'ctx_file_name' in the ctx 
    """

    @staticmethod
    def store_context():
        """
        Writes the current ctx to the disk
        """
        file_name = ctx().ctx_file_name
        with open(file_name, "wb") as ctxFile:
            pickle.dump(ctx(), ctxFile)
