######################################################
# Environment variables for VLibras-Linux (LAVID-UFPB)
#
# Author: CaioMoraes
# GitHub: MoraesCaio
# Email: caiomoraes.cesar@gmail.com
######################################################

# TODO: set correct values

import os
import re

# VALUES
home = os.environ['HOME']

env_vars = {
    'HUNPOS_TAGGER': f'{home}/new_hunpos',
    'AELIUS_DATA': f'{home}/new_aelius',
    'TRANSLATE_DATA': f'{home}/new_translate',
    'NLTK_DATA': f'{home}/new_nltk'
}

python_path_vals = [
    f'{home}/open-signs/vlibras-libs/aelius',
    f'{home}/open-signs/vlibras-translate/src',
    f'{home}/open-signs/vlibras-translate/src/Ingles',
    f'{home}/open-signs/vlibras-translate/src/Portugues',
    f'{home}/open-signs/vlibras-translate/src/Espanhol',
    f'{home}/open-signs/vlibras-translate/src/Templates',
]

old_path = 'VLibras-python3'

open_comment = f'\n\n# >>> Python and VLibras variables >>>\n'
close_comment = f'# <<< Python and VLibras variables <<<\n'

bashrc_file = f'{home}/.rc'
# END OF VALUES


def is_removable(line):
    if is_vlibras_var(line) or\
            open_comment[2:-2] in line or\
            close_comment[:-2] in line or\
            f'export PYTHONPATH' in line:
        return True
    return False


def is_vlibras_var(line):
    for var in env_vars:
        if f'{var}=' in line or\
                f'export {var}' in line:
            return True
    return False


with open(bashrc_file, 'r') as file:

    lines = []
    for line in file:

        # Catching current PYTHONPATH's value
        if f'PYTHONPATH=' in line:

            matches = re.match(fr'PYTHONPATH=\"(.*)\"', line)

            if matches:
                python_path = matches.groups()[0]
                paths = python_path.split(':')

                # Removing old values
                for path in paths:
                    if old_path not in path:
                        python_path_vals.append(path)

                continue

        if not is_removable(line):
            lines.append(line)

    # Appending new section to ~/.bashrc
    lines.append(open_comment)

    new_python_path = ':'.join(python_path_vals)
    lines.append(f'export PYTHONPATH=\"{new_python_path}\"\n')

    for var, val in env_vars.items():
        lines.append(f'export {var}=\"{val}\"\n')

    lines.append(close_comment)

# Rewriting file
with open(bashrc_file, 'w') as file:
    file.writelines(lines)
