from navec import Navec
from slovnet import NER
from natasha import (
    Segmenter,

    NewsEmbedding,
    NewsMorphTagger,


    Doc
)

class NERParser:
    def __init__(self, navec_weights: str, ner_weights: str) -> None:
        self.navec = Navec.load(navec_weights)
        self.ner = NER.load(ner_weights)
        self.ner.navec(self.navec)
        self.emb = NewsEmbedding()
        self.morph_tagger = NewsMorphTagger(self.emb)
        self.segmenter = Segmenter()

    def get_ners_dict(self, text: str) -> dict:
        """ Returns a dictionary of named entities in a text
            Args:
                text (str): text to parse
                ner_model (slovnet.NER): ner model
            Returns:
                dict: dictionary of named entities in a text
            """
            # Use this function with pandarallel's parallel_apply
        if not text:
            return {'ORGs': [], 'PERs': [], 'LOCs': [], 'NOUs': []}
        markup = self.ner(text)
        ORGS, PERS, LOCS = [], [], []
        for span in markup.spans:
            span_text = markup.text[span.start:span.stop]
            {
                'ORG': ORGS,
                'PER': PERS,
                'LOC': LOCS,

            }[span.type].append(span_text)
            # print(span.type, span_text)
        # Получить существительные из текста
        doc = Doc(text)
        doc.segment(self.segmenter)
        doc.tag_morph(self.morph_tagger)
        nouns = [_.text for _ in doc.tokens if _.pos == 'NOUN']
        # print(nouns)
        return {'ORGs': ORGS if ORGS else [], 'PERs': PERS if PERS else [], 'LOCs': LOCS if LOCS else [], 'NOUs': nouns}




if __name__ == '__main__':
    from ipymarkup import show_span_ascii_markup as show_markup
    text = """
    Генеральный директор Первого канала Константин Эрнст рассказал о том, как осуществляется контроль за контентом на российском телевидении. Комментарий медиаменеджера опубликован в журнале New Yorker. «Никто никогда не говорит вам: "Не показывайте Навального (Алексей Навальный, блогер — прим. «Ленты.ру»), не используйте его имя". Такие поручения не передаются словами», — так Эрнст ответил на вопрос о том, есть ли цензура на телевидении. Он добавил, что федеральными каналами руководят неглупые люди. Телеведущая Юлия Панкратова, работавшая на Первом канале с 2006 по 2013 год, подтвердила, что в большинстве случаев сотрудникам не поступало прямых указаний от руководства по поводу контента. В беседе с журналистом New Yorker она призналась, что от нее чаще ожидали интуитивного понимания правил. Константин Эрнст возглавляет Первый канал с 1999 года. Он начал карьеру на телевидении в 1988 году в программе «Взгляд», затем стал автором и ведущим программы «Матадор». С 6 октября 1999 года журналист является генеральным директором ОРТ (с 2002 года компания называется «Первый канал»). Ранее комик и телеведущий Максим Галкин заявил о цензуре на российском телевидении. Он заметил, что раньше на российских телеканалах было больше политического юмора, однако сегодня «не все можно говорить».
    """
    ner = NERParser(
        r"S:\Workspace\MORETECH\nlp-workbench\models\navec_news_v1_1B_250K_300d_100q.tar",
        r"S:\Workspace\MORETECH\nlp-workbench\models\slovnet_ner_news_v1.tar",
    )
    markup = ner.ner(text)
    print(show_markup(markup.text, markup.spans))


