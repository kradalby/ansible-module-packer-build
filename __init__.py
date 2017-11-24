#!/usr/bin/python

__author__ = 'kradalby'

import os.path


def main():
    module = AnsibleModule(
        argument_spec=dict(
            packer_path=dict(default="", type='str'),
            template_dir=dict(required=True, type='str'),
            template=dict(required=True, type='str'),
            variable=dict(default="", type='str')),
        supports_check_mode=True,
    )

    packer_exec = 'packer' if not module.params['packer_path'] else '{}/packer'.format(
        module.params['packer_path'])

    if not os.path.isfile(packer_exec):
        module.fail_json(msg='Could not find packer, is the path correct: {}?'.
                         format(packer_exec))

    template_file = os.path.join(module.params['template_dir'],
                                 module.params['template'])
    if not os.path.isfile(template_file):
        module.fail_json(
            msg='Could not find template, is the path correct: {}?'.format(
                template_file))

    command_tokens = [packer_exec]

    command_tokens.extend([
        'build',
    ])

    if module.params['variable']:
        command_tokens.extend(
            ['-var-file={}'.format(module.params['variables'])])

    command_tokens.extend([template_file])

    ova_tool_result = module.run_command(
        command_tokens, cwd=module.params['template_dir'])

    if ova_tool_result[0] != 0:
        module.fail_json(
            msg=
            'Failed to create virtual machine image, error message from packer is: {}'.
            format(ova_tool_result[1]))

    module.exit_json(changed=True, ova_tool_result=ova_tool_result)


from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()
