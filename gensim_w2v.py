import spacy
import pandas as pd
from gensim.models import Word2Vec
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt


class Word2VecClass:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_lg')

    def getcontents(self, df):
        '''

        :param df:
        :return:
        '''

        df.Contents = df.Contents.apply(lambda x: str(x))
        contents = df['Contents'].str.lower().str.strip().values.tolist()
        return contents

    def getlemmapos(self, contents):
        '''

        :param contents:
        :return:
        '''
        pjt_list_lemma = []
        pjt_list_pos = []

        for idx, doc in enumerate(self.nlp.pipe(contents)):

            print(idx, "/", len(contents))

            nlp_text = self.nlp(doc.text)
            temp_list_lemma = []
            temp_list_pos = []

            for word in nlp_text:
                temp_list_lemma.append(word.lemma_)
                temp_list_pos.append(word.pos_)

            pjt_list_lemma.append(temp_list_lemma)
            pjt_list_pos.append(temp_list_pos)

        return pjt_list_lemma, pjt_list_pos

    def cleandata(self, pjt_list_lemma, pjt_list_pos):
        '''

        :param pjt_list_lemma:
        :param pjt_list_pos:
        :return:
        '''
        pos_list = ['ADJ', 'ADP', 'ADV', 'AUX', 'CONJ', 'CCONJ', 'DET', 'INTJ',
                    'PART', 'PUNCT', 'SCONJ', 'SYM', 'VERB', 'X']
        index_list = []

        for index1, value1 in enumerate(pjt_list_pos):
            # print(index1, value1)
            temp_index_list = []
            for index2, value2 in enumerate(pjt_list_pos[index1]):
                if value2 not in pos_list:
                    temp_index_list.append(index2)
            index_list.append(temp_index_list)

        pjt_list_lemma_update = []

        for index, (index_value, lemma_value) in enumerate(zip(index_list, pjt_list_lemma)):
            temp_lemma_update = []
            for noun_index in index_value:
                temp_lemma_update.append(lemma_value[noun_index])
            pjt_list_lemma_update.append(temp_lemma_update)

        item_list = ['-PRON-', '.', ',', '!', '?', '$', '#', '=', '*', '/', '[', ']',
                     '（', '(', ')', '）', '-', '–', ':', '️', '  ', 'rt', '\n', '\n ',
                     ';', '…', '...', '....', '️', '_', '>', '<', '|', '"', "'"]

        pjt_list = []
        for lst in pjt_list_lemma_update:
            temp_list = []
            for element in lst:
                if element not in item_list:
                    if 'https://' not in element and 'http://' not in element and '@' not in element:
                        temp_list.append(element)
            pjt_list.append(temp_list)

        return pjt_list

    def list_data(self, pjt_list):
        '''

        :param pjt_list:
        :return:
        '''
        for index in range(len(pjt_list)):
            print(pjt_list[index])
            print("##########################################")

    def trainandplot(self, pjt_list, name, minimum_count=5500):
        '''

        :param pjt_list:
        :param name:
        :param minimum_count:
        :return:
        '''
        # train
        sentences = pjt_list
        model = Word2Vec(size=150, window=5, min_count=minimum_count, seed=123, workers=10, iter=10) # Word2Vec(size=150, window=10, min_count=2, workers=10, iter=10)
        model.build_vocab(sentences)
        model.train(sentences, total_examples=model.corpus_count, epochs=model.iter)  # train word vectors # >> corpus_count >> tf-idf

        #test
        w1 = 'camera'
        print(model.wv.most_similar(positive=w1))

        # plot
        vocab = list(model.wv.vocab)
        X = model[vocab]
        tsne = TSNE(n_components=2)
        X_tsne = tsne.fit_transform(X)
        df = pd.DataFrame(X_tsne, index=vocab, columns=['x', 'y'])

        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.scatter(df['x'], df['y'])

        for word, pos in df.iterrows():
            ax.annotate(word, pos)

        # plt.show()
        ax.get_figure().savefig('./output/w2v/{}.png'.format(name))

    def main(self):
        '''

        :return:
        '''
        df = pd.read_csv('./data/buzz/monitor_30712419356_01-01-2019_11-30-2019.rawdata')
        contents = self.getcontents(df)
        pjt_list_lemma, pjt_list_pos = self.getlemmapos(contents)
        pjt_list = self.cleandata(pjt_list_lemma, pjt_list_pos)
        self.trainandplot(pjt_list)


if __name__ == '__main__':
    samsung = pd.read_csv('./data/buzz/monitor_30712419356_01-01-2019_11-30-2019.rawdata') # samsung
    apple = pd.read_csv('./data/buzz/monitor_30712424624_01-01-2019_10-31-2019.rawdata') # apple
    huawei = pd.read_csv('./data/buzz/monitor_30712429893_01-01-2019_11-30-2019.rawdata') # huawei
    google = pd.read_csv('./data/buzz/monitor_30712434662_01-01-2019_11-30-2019.rawdata') # google

    w2v = Word2VecClass()
    contents = w2v.getcontents(samsung)
    pjt_list_lemma, pjt_list_pos = w2v.getlemmapos(contents)
    pjt_list = w2v.cleandata(pjt_list_lemma, pjt_list_pos)
    w2v.trainandplot(pjt_list, name, minimum_count)
