def validate_account_request(pwrd1, pwrd2):
    if pwrd1 == pwrd2:
        return ""
    return "Password not correct"