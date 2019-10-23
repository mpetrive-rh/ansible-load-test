# -*- mode: python -*-

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import sys
#from ansible.errors import AnsibleError
from ansible.plugins.action import ActionBase
import ctypes

try:
    from __main__ import display
except ImportError:
    from ansible.utils.display import Display
    display = Display()

class ActionModule(ActionBase):

    def run(self, tmp=None, task_vars=None):

        self._supports_check_mode = False

        result = super(ActionModule, self).run(tmp, task_vars)
        del tmp  # tmp no longer has any effect

        fact_size = int(self._task.args.get('size', 1))
        py_byte_size = fact_size * (2**20)
        s = ctypes.create_string_buffer(py_byte_size)
        ctypes.memset(ctypes.addressof(s), 65, ctypes.sizeof(s))

        result = {}
        result['changed'] = False
        bff = s.value
        result['ansible_facts'] = { 'big_fact' : bff, 'big_fact_size' : sys.getsizeof(bff) }
        del s
        return result
