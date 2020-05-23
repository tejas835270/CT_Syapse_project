import os
import sys
import pytest

def gettoken():
    """
    Purpose : This method is useful to get jwt token value using web service credentials.
    :return: jwt token string
    """
    from qa_automation_drt_haw.api.api_utils.serviceApi import Token
    from qa_automation_drt_haw.settings import Config
    username = Config.portal_2_roles_username
    psw = Config.portal_2_roles_password

    valid_jwt = Token(username, psw)
    return str(valid_jwt)


def main():
    """
    Purpose : This method is used to generate jwt token value from command line
    :return: Returns the jwt token value in string format
    example: In command line (terminal), navigate till directory for jwt_token.py and run command
    python jwt_token.py <env>
    """
    os.environ['ENV'] = sys.argv[1]
    pytest.env = sys.argv[1]
    token = gettoken()
    print(token)


if __name__ == "__main__":
    main()
