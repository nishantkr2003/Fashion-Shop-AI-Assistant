from argon2 import PasswordHasher

ph = PasswordHasher()


def hash_password(
    password:str
):

    return ph.hash(
        password
    )


def verify_password(
    password:str,
    hashed:str
):

    try:

        ph.verify(
            hashed,
            password
        )

        return True

    except:

        return False