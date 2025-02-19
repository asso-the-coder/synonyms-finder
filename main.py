#Asser Abdelgawad and Yousef AlRawwash - Project 3: Synonyms - 7/12/2021

import math

def norm(vec):
    '''Return the norm of a vector stored as a dictionary,
    as described in the handout for Project 3.
    '''

    sum_of_squares = 0.0
    for x in vec:
        sum_of_squares += vec[x] * vec[x]

    return math.sqrt(sum_of_squares)


def cosine_similarity(vec1, vec2):

  #initialize
  sim_keys = []
  numerator = 0
  denominator = 2

  #find similar words in vec1 and vec2
  for keys in vec1:
    if keys in vec2:
     sim_keys.append(keys)

  #computing dot products of all similar strings in vec1 and vec2 and adding each similar entry to the one before
  for key in sim_keys:
    numerator += vec1[key] * vec2[key]

  #magnitudes of the vectors
  denominator = (norm(vec1)*norm(vec2))

  #compute cosine similarity
  return numerator/denominator

def is_coming_in_sentence(cur_ind,cur_word, current_sentence):
    list_other_than_cur_word = current_sentence[cur_ind+1:]
    if cur_word in list_other_than_cur_word:
            return True
    return False

def build_semantic_descriptors(sentences):

    dic = {}

    for i in range(len(sentences)):
        for j in range(len(sentences[i])):
            dic[sentences[i][j]] = {}

    for current_sentence in sentences:
        for cur_ind in range(len(current_sentence)):
            current_word = current_sentence[cur_ind].lower()
            if not is_coming_in_sentence(cur_ind, current_word, current_sentence):
                for other_ind in range(len(current_sentence)):
                    other_words = current_sentence[other_ind].lower()

                    if other_words != current_word:
                        if not is_coming_in_sentence(other_ind, other_words, current_sentence):
                            if other_words in dic[current_word]:
                                dic[current_word][other_words] += 1
                            elif other_words not in dic[current_word]:
                                dic[current_word][other_words] = 1





    return dic



def build_semantic_descriptors_from_files(filenames):
    dic = {}
    all_sentences = []
    total_list = []
    altered_file = ""

    for i in range(len(filenames)):
        current_file = open(filenames[i],"r",encoding = "latin1")
        temp_file = current_file.read()
        altered_file = temp_file.lower()

        mid_sentence_punc = [",", "-", "--", ":", ";"]

        for i in range(len(mid_sentence_punc)):
            altered_file = altered_file.replace(mid_sentence_punc[i], " ")

        all_sentences = altered_file.replace("!", ".").replace("?", ".").split(".")

        for each_sentence in all_sentences:
            total_list.append(each_sentence.split())

    dic = build_semantic_descriptors(total_list)

    return dic


def most_similar_word(word, choices, semantic_descriptors, similarity_fn):

  similarities = {}
  max_similarity = -1
  best_choice = ""

  for choice in choices:
    if word in semantic_descriptors and choice in semantic_descriptors:
      
      similarities[choice] = similarity_fn(semantic_descriptors[word], semantic_descriptors[choice])

      if similarities[choice] > max_similarity:
        max_similarity = similarities[choice]
        best_choice = choice
    else:
        similarities[choice] = -1
  
  return best_choice

def run_similarity_test(filename, semantic_descriptors, similarity_fn):

  words = []

  #read file
  lines = open(filename, encoding = "latin1")
  lines = lines.read()
  lines = lines.split("\n")

  if lines[-1] == "":
    lines.pop()

  sentence = []
  for i in range(len(lines)):
    sentence.append(lines[i])

  for i in range(len(sentence)):
    words.append(sentence[i].split(" "))

  sim_list = []
  correct = 0
  
  for i in range(len(words)):
    sim_list.append(most_similar_word(words[i][0], words[i][2:], semantic_descriptors, similarity_fn))

    if sim_list[i] == words[i][1]:
      correct += 1
  
  if "" in sim_list:
    sim_list.remove("")
  
  return (correct/len(sim_list))*100


if __name__ == '__main__':
  #print(cosine_similarity({"a": 1, "b":2, "c": 3}, {"b":4, "c":5, "d":6}))

  #print(build_semantic_descriptors([["i", "am", "a", "sick", "man"], ["hi","how","are","a", "a"]]))

  sem_descriptors = build_semantic_descriptors_from_files(["wp.txt", "sw.txt"])
  res = run_similarity_test("test.txt", sem_descriptors, cosine_similarity)
  print(res, "% of the guesses were correct")