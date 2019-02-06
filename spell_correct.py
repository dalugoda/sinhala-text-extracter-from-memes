import codecs


def search_nested(arr, val):

    for i in range(len(arr)):
        # loops j from 0 to num of cols in each row
        for j in range(len(arr[i])):
            # print i, j  # my own debugging commented out
            # compare each cell to search value
            if arr[i][j] == val:
                # if found, return entire row that the value was found in
                return arr[i]
    # if value not found, return a string instead
    return []


def get_character_groups():
    group_file = codecs.open("character_groups.txt", "r", "utf-8")
    groups = []
    lines = group_file.read().split("\n")

    for line in lines:
        characters = line.split("\t")
        group = []
        for char in characters:
            group.append(char.replace("\r", ""))

        groups.append(group)

    group_file.close()

    return groups


def generate_permutations(char_groups, word, char_index):
    if char_index == len(word):
        return []

    permutation_list = set()

    for x in range(char_index, len(word)):

        c = word[x]
        sm_group = search_nested(char_groups, c)

        if len(sm_group) > 0:
            for e in sm_group:
                comb = word[:x] + e + word[x + 1:]
                if str(comb) not in permutation_list:

                    permutation_list.add(comb)

                    result = generate_permutations(char_groups, comb, char_index + 1)
                    for res in result:
                            permutation_list.add(res)

    return permutation_list


def get_corpus_word_set():
    word_set = set()
    file = codecs.open('facebook_words.txt', 'r', encoding="utf-8")
    lines = file.read().split("\n")
    for line in lines:
        words = line.split(" ")
        for word in words:
            word_set.add(word.strip())

    file.close()
    print(len(word_set))

    return word_set


def spell_correct(sentence):
    print("Spelling Correction Started...")
    sentence_words = sentence.split(" ")
    corpus_words = get_corpus_word_set()
    char_groups = get_character_groups()
    output = []
    corrected_count = 0
    for sentence_word in sentence_words:
        if sentence_word in corpus_words:
            output.append(sentence_word)
        else:
            permutations = generate_permutations(char_groups, sentence_word, 0)
            permutation_found = False
            for permutation in permutations:
                if permutation in corpus_words:
                    permutation_found = True
                    corrected_count += 1
                    output.append(permutation)
                    break

            if not permutation_found:
                output.append(sentence_word)

    print(corrected_count, " words corrected.")
    print("Process Completed !")
    return " ".join(output)

