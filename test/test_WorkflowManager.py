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
Tests for `ivy.WorkflowManager` module.

author: jakeret
"""

from getopt import GetoptError
from operator import eq

import pytest

from ivy import workflow_manager
from ivy.context import ctx
from ivy.exceptions.exceptions import InvalidAttributeException
from ivy.loop import Loop
from ivy.workflow_manager import WorkflowManager
from test.ctx_sensitive_test import ContextSensitiveTest


class TestWorkflowManager(ContextSensitiveTest):

    def test_launch(self):
        args = ["test.config.workflow_config"]

        mgr = WorkflowManager(args)
        mgr.launch()

        assert ctx() is not None
        assert ctx().params is not None
        assert ctx().params.plugins is not None

    def test_parseArgs(self):
        args = ["--a=True",
                "--b=False",
                "--c=-1",
                "--d=0",
                "--e=1",
                "--f=-1.0",
                "--g=0.0",
                "--h=1.0",
                "--i=le_string",
                "--j=1,2,3,4",
                "--bool1=True",
                "--bool2=False",
                "--bool3=True",
                "--bool4=False",
                "test.config.workflow_config"]

        mgr = WorkflowManager(args)

        assert ctx().params.a == True
        assert ctx().params.b == False
        assert ctx().params.c == -1
        assert ctx().params.d == 0
        assert ctx().params.e == 1
        assert ctx().params.f == -1.0
        assert ctx().params.g == 0.0
        assert ctx().params.h == 1.0
        assert ctx().params.i == "le_string"
        assert ctx().params.bool1 == True
        assert ctx().params.bool2 == False
        assert ctx().params.bool3 == True
        assert ctx().params.bool4 == False
        assert all(map(eq, ctx().params.j, [1, 2, 3, 4]))

    def test_simple_launch(self):
        args = ["test.config.workflow_config_simple"]

        mgr = WorkflowManager(args)
        mgr.launch()

        assert ctx() is not None
        assert ctx().params is not None
        assert ctx().params.plugins is not None
        assert isinstance(ctx().params.plugins, Loop)

    def test_missing_plugins(self):
        args = ["ivy.config.base_config"]

        try:
            mgr = WorkflowManager(args)
            pytest.fail("config without plugins not allowed", True)
        except InvalidAttributeException:
            assert True

    def test_missing_config(self):
        try:
            mgr = WorkflowManager(None)
            pytest.fail("missing config not allowed", True)
        except InvalidAttributeException:
            assert True

        try:
            mgr = WorkflowManager([])
            pytest.fail("missing config not allowed", True)
        except InvalidAttributeException:
            assert True

    def test_invalid_config(self):
        args = ["test.config.workflow_config_simple", "test.config.workflow_config_simple"]
        try:
            mgr = WorkflowManager(args)
            pytest.fail("two configs not allowed", True)
        except InvalidAttributeException:
            assert True

    def test_invalid_args(self):
        args = ["-a=1",
                "test.config.workflow_config_simple"]
        try:
            mgr = WorkflowManager(args)
            pytest.fail("wrong argument format", True)
        except GetoptError:
            assert True

    def test_unknown_args(self):
        args = ["--a=1",
                "test.config.workflow_config_simple"]
        try:
            mgr = WorkflowManager(args)
            pytest.fail("wrong argument format", True)
        except GetoptError:
            assert True

    def test_load_configs_invalid(self):
        try:
            _ = workflow_manager.load_configs(None)
            pytest.fail("No config name not allowed", True)
        except InvalidAttributeException:
            assert True

    def test_load_configs_one_arg(self):
        config = workflow_manager.load_configs("test.config.workflow_config_args")
        assert config is not None
        assert config.conf_arg_int == 1
        assert config.conf_arg_float == 1.0
        assert config.conf_arg_str == "1"

    def test_load_configs_multiple_arg(self):
        config = workflow_manager.load_configs(["test.config.workflow_config_args",
                                                "test.config.workflow_config"])
        assert config is not None

        # from workflow_config_args
        assert config.conf_arg_int == 1
        assert config.conf_arg_float == 1.0
        assert config.conf_arg_str == "1"

        # from workflow_config
        assert config.a == None
        assert config.b == None

    def test_load_configs_overwrite(self):
        config = workflow_manager.load_configs("test.config.workflow_config_args")
        assert config is not None
        assert config.conf_arg_int == 1

        config.conf_arg_int = 2
        assert config.conf_arg_int == 2

    def test_create_from_dict(self):
        args = {"plugins": ["test.plugin.simple_plugin", "test.plugin.simple_plugin"],
                "a": 1
                }
        mgr = WorkflowManager(args)
        assert ctx().params is not None
        assert ctx().params.a is 1
        assert ctx().params.plugins is not None
        plugins = [p for p in ctx().params.plugins]
        assert len(plugins) is 2

    def teardown(self):
        # tidy up
        print("tearing down " + __name__)
        pass


if __name__ == '__main__':
    pytest.main("-k TestWorkflowManager")
