import spacy
from spacy.language import Language
import re


class TextCleaner:
    """
    A class used to remove common sentences from a given text using
    regex or spaCy similarity.


    ...

    Attributes
    ----------
    common_sentences : list
        a list of common sentences to remove from the text
    nlp : Language
        a spaCy Language object, used to process the text and compute
        similarities
    similarity_threshold : float
        the similarity score above which a sentence is considered
        "common"
    common_regex_patterns : list
        a list of compiled regex patterns corresponding to the common
        sentences

    Methods
    -------
    remove_common_sentences(text: str) -> str:
        Removes the common sentences from the given text and returns the
        cleaned text.
    _is_common_spacy(sentence) -> bool:
        Checks if a given sentence is similar to any of the common
        sentences using spaCy similarity.
    _is_common_regex(sentence: str) -> bool:
        Checks if a given sentence matches any of the common sentences
        using regular expressions.
    """

    def __init__(
        self,
        common_sentences: list,
        nlp: Language,
        similarity_threshold: float = 0.85,
    ):
        """
        Constructs all the necessary attributes for the TextCleaner
        object.


        Parameters
        ----------
        common_sentences : list
            a list of common sentences to remove from the text
        nlp : Language
            a spaCy Language object, used to process the text and
            compute similarities
        similarity_threshold : float, optional
            the similarity score above which a sentence is considered
            "common" (default is 0.85)
        """
        self.common_sentences = [
            nlp(sentence) for sentence in common_sentences
        ]
        self.nlp = nlp
        self.similarity_threshold = similarity_threshold
        self.common_regex_patterns = [
            re.compile(re.escape(sentence), re.IGNORECASE)
            for sentence in common_sentences
        ]

    def remove_common_sentences(self, text: str) -> str:
        """
        Removes the common sentences from the given text using regex and
        spaCy similarity.

        Parameters
        ----------
        text : str
            the text to clean

        Returns
        -------
        str
            the cleaned text, with all common sentences removed
        """
        result_sentences = []
        for sentence in self.nlp(text).sents:
            if not self._is_common_regex(
                sentence.text
            ) and not self._is_common_spacy(sentence):
                result_sentences.append(sentence.text)
        return " ".join(result_sentences)

    def _is_common_spacy(self, sentence) -> bool:
        """
        Checks if a given sentence is similar to any of the common
        sentences using spaCy similarity.

        Parameters
        ----------
        sentence : spacy.tokens.Span
            the sentence to check

        Returns
        -------
        bool
            True if the sentence is similar to a common sentence, False
            otherwise
        """
        for common_sentence in self.common_sentences:
            if (
                sentence.similarity(common_sentence)
                > self.similarity_threshold
            ):
                return True
        return False

    def _is_common_regex(self, sentence: str) -> bool:
        """
        Checks if a given sentence matches any of the common sentences
        using regular expressions.

        Parameters
        ----------
        sentence : str
            the sentence to check

        Returns
        -------
        bool
            True if the sentence matches a common sentence, False
            otherwise
        """
        return any(
            pattern.search(sentence) for pattern in self.common_regex_patterns
        )