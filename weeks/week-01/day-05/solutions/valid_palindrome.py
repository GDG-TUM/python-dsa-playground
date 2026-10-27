def is_palindrome(s):
    # TODO: ignore case and non-alphanumeric characters
    pass


if __name__ == "__main__":
    assert is_palindrome("A man, a plan, a canal: Panama") is True
    assert is_palindrome("race a car") is False
    assert is_palindrome(" ") is True
    print("All tests passed")
