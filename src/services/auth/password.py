import string

__all__ = ["AuthInfoValidationService", "TooShortPasswordError", "TooLongPasswordError"]

class AuthInfoValidationService:
    __min_passwd_len = 8
    __max_passwd_len = 32
    __allowed_passwd_symbols = set(string.ascii_letters + string.digits + "_-")

    __min_username_len = 6
    __max_username_len = 32
    __allowed_username_symbols = set(string.ascii_letters + string.digits + "_-")

    def ValidatePassword(self, password: str):
        if len(password) < self.__min_passwd_len:
            raise TooShortPasswordError(f"Minimal password length: {self.__min_passwd_len}")
        if len(password) > self.__max_passwd_len:
            raise TooLongPasswordError(f"Maximal password length: {self.__max_passwd_len}")
        if not set(password).issubset(self.__allowed_passwd_symbols):
            raise IncorrectSymbolsError(f'"{password}" is not a valid symbol. allowed symbols: {self.__allowed_passwd_symbols}')


    def ValidateUsername(self, username: str):
        if len(username) < self.__min_username_len:
            raise TooShortUsernameError(f"Minimal username length: {self.__min_username_len}")
        if len(username) > self.__max_username_len:
            raise TooLongUsernameError(f"Maximal username length: {self.__max_username_len}")
        if not set(username).issubset(self.__allowed_username_symbols):
            raise IncorrectSymbolsError(f'"{username}" is not a valid symbol. allowed symbols: {self.__allowed_username_symbols}')

    def Validate(self, username: str, password: str):
        self.ValidateUsername(username)
        self.ValidatePassword(password)

class TooShortPasswordError(Exception):
    pass

class TooLongPasswordError(Exception):
    pass

class IncorrectSymbolsError(Exception):
    pass

class TooShortUsernameError(Exception):
    pass

class TooLongUsernameError(Exception):
    pass