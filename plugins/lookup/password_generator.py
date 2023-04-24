import secrets
import string
from ansible.errors import AnsibleError, AnsibleParserError
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display

display = Display()

class LookupModule(LookupBase):
    VALID_PARAMS = frozenset((
        'length',
        'min_lower_chars',
        'max_lower_chars',
        'min_upper_chars',
        'max_upper_chars',
        'min_digits',
        'max_digits',
        'min_special_chars',
        'max_special_chars',
        'special_chars',
        'max_attempts',
    ))

    def __gen_password(
        self,

        length: int,
        max_attempts: int,

        min_lower_chars: int,
        max_lower_chars: int,

        min_upper_chars: int,
        max_upper_chars: int,

        min_special_chars: int,
        max_special_chars: int,
        special_chars: str,

        min_digits: int,
        max_digits: int,
        ):

        if min_lower_chars > max_lower_chars:
            min_lower_chars = max_lower_chars
        if min_upper_chars > max_upper_chars:
            min_upper_chars = max_upper_chars
        if min_digits > max_digits:
            min_digits = max_digits
        if min_special_chars > max_special_chars:
            min_special_chars = max_special_chars

        alphabet = ''
        if max_lower_chars != 0:
            alphabet += string.ascii_lowercase
        if max_upper_chars != 0:
            alphabet += string.ascii_uppercase
        if max_digits != 0:
            alphabet += string.digits
        if max_special_chars != 0 and special_chars:
            alphabet += special_chars

        if not alphabet:
            raise AnsibleError('Incorrect password settings, resulting to empty alphabet')

        success = False

        # generate initial password
        password = ''.join(secrets.choice(alphabet) for i in range(length))

        for i in range(max_attempts):
            lowers = 0
            uppers = 0
            digits = 0
            specials  = 0

            for c in password:
                if c.islower():
                    lowers += 1
                elif c.isupper():
                    uppers += 1
                elif c.isdigit():
                    digits += 1
                else:
                    specials += 1

            if lowers >= min_lower_chars and lowers <= max_lower_chars \
                and uppers >= min_upper_chars and uppers <= max_upper_chars\
                and digits >= min_digits and digits <= max_digits \
                and specials >= min_special_chars and specials <= max_special_chars:
                    success = True
                    display.debug('Generated password after %d attempts' % i)
                    break

            # shift password by 1 char and repeat checks
            password = password[1:] + secrets.choice(alphabet)

        if not success:
            raise AnsibleError('Failed to generate random password with the specified settings after %d attempts' % max_attempts)

        return password


    def run(self, terms, variables=None, **kwargs):
        self.set_options(var_options=variables, direct=kwargs)

        invalid_params = frozenset(kwargs.keys()).difference(self.VALID_PARAMS)
        if invalid_params:
            raise AnsibleError('Unrecognized parameter(s) given: %s, possible params: %s' % (
                ', '.join(invalid_params),
                ', '.join(self.VALID_PARAMS)
            ))

        password = self.__gen_password(
            length=int(kwargs.get('length', 16)),
            min_lower_chars=int(kwargs.get('min_lower_chars', 1)),
            max_lower_chars=int(kwargs.get('max_lower_chars', 6)),
            min_upper_chars=int(kwargs.get('min_upper_chars', 1)),
            max_upper_chars=int(kwargs.get('max_upper_chars', 6)),
            min_special_chars=int(kwargs.get('min_special_chars', 1)),
            max_special_chars=int(kwargs.get('max_special_chars', 6)),
            special_chars=str(kwargs.get('special_chars', '~-_,.!%^*')),
            min_digits=int(kwargs.get('min_digits', 1)),
            max_digits=int(kwargs.get('max_digits', 6)),
            max_attempts=int(kwargs.get('max_attempts', 10000)),
        )

        return [password]
