#! -*- coding:utf-8 -*-
import codecs
import re
# import jieba


def lcs(string1_list, string2_list):
    n = len(string1_list)
    m = len(string2_list)

    if m == 0 or n == 0:
        return -1
    c = [[0 for _ in range(m + 1)] for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if string1_list[i - 1] == string2_list[j - 1]:
                c[i][j] = c[i - 1][j - 1] + 1
            else:
                c[i][j] = max(c[i][j - 1], c[i - 1][j])
    return c[-1][-1]

def read_data():
    data = codecs.open('test.doc_query', encoding='utf-8').read()
    data = re.split('\n', data)[:-1]
    # print(len(data))
    text = []
    question = []
    one_text = []
    for line in data:
        head, content = line.split(' ||| ')
        if 'qid' in head:
            one_question = content.split(" ")
            if one_question[-1] in ['？', '?']:
                one_question = one_question[:-1]
            question.append(one_question)
            text.append(one_text)
            one_text = []
        else:
            one_text_line = content.split(" ")
            one_text.extend(one_text_line)
    assert len(text) == len(question)
    return text, question

def read_stopwords():
    stopwords = codecs.open('stop_words.txt', encoding='utf-8').read()
    stopwords = stopwords.split("\n")
    return stopwords

def get_most_lcs_sentence(text, question):
    sentences = []
    start_idx = 0
    for i in range(len(text)):
        word = text[i]
        if word in ['，', '。', '！', '：', '……', '？', ',', '?', '；', ';',  '.']:
            if i > start_idx:
                sentence = text[start_idx: i]
                sentences.append(sentence)
                start_idx = i + 1
        if i == len(text) - 1 and i >= start_idx:
            sentence = text[start_idx:]
            sentences.append(sentence)

    most_lcs_sentence = []
    most_lcs_length = 0
    for sen in sentences:
        lcs_lenght = lcs(sen, question)
        if lcs_lenght > most_lcs_length:
            most_lcs_length = lcs_lenght
            most_lcs_sentence = sen

    return most_lcs_sentence

def extract_answer(sentence, question):
    que_words = ['什么', '哪里', '谁', '哪', '哪儿', '什么样', '怎么']
    answer = []
    for qw in que_words:
        if qw in question:
            que_len = len(question)
            qw_index = question.index(qw)
            qw_b_index = qw_index - 1
            qw_a_index = qw_index + 1
            if qw_b_index < 0:
                # pass
                while qw_a_index < que_len-1 and question[qw_a_index] not in sentence :
                    qw_a_index += 1
                if question[qw_a_index] in sentence:
                    answer = sentence[:sentence.index(question[qw_a_index])]
                else:
                    answer = sentence[:qw_a_index]
            elif qw_a_index >= que_len:
                # pass
                while qw_b_index > 0 and question[qw_b_index] not in sentence :
                    qw_b_index -= 1
                if question[qw_b_index] in sentence:
                    answer = sentence[sentence.index(question[qw_b_index])+1:]
                else:
                    answer = sentence[qw_b_index:]
            else:
                while qw_a_index < que_len - 1 and question[qw_a_index] not in sentence :
                    qw_a_index += 1
                while qw_b_index > 0 and question[qw_b_index] not in sentence:
                    qw_b_index -= 1
                if question[qw_b_index] in sentence:
                    start_index = sentence.index(question[qw_b_index])+1
                    if start_index >= len(sentence) - 1:
                        start_index -= 1
                else:
                    start_index = qw_b_index

                if question[qw_a_index] in sentence:
                    end_index = sentence.index(question[qw_a_index])
                    if end_index <= 0 :
                        end_index += 1
                else:
                    end_index = qw_a_index
                answer = sentence[start_index:end_index]

                # if abs(qw_index - qw_b_index) <= 1:
                #     if question[qw_b_index] in sentence:
                #         answer = [].append(sentence[start_index])
                # elif 1 >= abs(qw_index - qw_a_index):
                #     if question[qw_a_index] in sentence:
                #         answer = [].append(sentence[end_index - 1])

    return answer


def main():
    # lcs_list = lcs(['1', '2', '3','3','3'], ['1','3','3'])
    # print(lcs_list)
    text, question = read_data()
    stopwords = read_stopwords()
    most_lcs_sentences = []
    for i in range(len(text)):
        most_lcs_sentence = get_most_lcs_sentence(text[i], question[i])
        most_lcs_sentences.append(most_lcs_sentence)
    most_lcs_sentences = [[word for word in sen if (word not in stopwords)] for sen in most_lcs_sentences]
    question = [[word for word in sen if (word not in stopwords)] for sen in question]

    assert len(most_lcs_sentences) == len(question)
    # for i in range(len(question)):
    #     print(i)
    #     print(most_lcs_sentences[i])
    #     print(question[i])

    answers = []
    for i in range(len(question)):
        # print(i)
        answer = extract_answer(most_lcs_sentences[i], question[i])
        answers.append(answer)

    with open('test.output.txt', 'w', encoding='utf-8') as f:
        for i in range(len(answers)):
            if len(answers[i]) == 0:
                answers[i] = most_lcs_sentences[i]
            f.write('<qid_' + str(i) + '> ||| ' + ''.join(answers[i]) + '\n')


if __name__ == '__main__':
   main()
   # answer = extract_answer(['厨师', '看见', '狗尾巴', '那里', '四处', '乱', '摇'], ['谁', '看见', '狗尾巴', '四处', '乱', '摇'])
   # print(answer)