def group_anagrams(strs):
    # TODO: group words that are anagrams of each other
    pass


def normalise(groups):
    return sorted(sorted(g) for g in groups)


if __name__ == "__main__":
    words = ["eat", "tea", "tan", "ate", "nat", "bat"]
    expected = [["bat"], ["nat", "tan"], ["ate", "eat", "tea"]]
    assert normalise(group_anagrams(words)) == normalise(expected)
    assert normalise(group_anagrams([""])) == [[""]]
    assert normalise(group_anagrams(["a"])) == [["a"]]
    print("All tests passed")
