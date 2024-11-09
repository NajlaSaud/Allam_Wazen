from .utils import (
    BOHOUR_NAMES,
    find_mismatch,
    label2name,
    char2idx,
    override_auto_tashkeel,
    vocab,
    BOHOUR_NAMES_AR,
)
from .utils import clean
import tkseem as tk
from sentence_transformers import util
from .Bohour.bohour.arudi_style import get_arudi_style
from .Bohour.bohour.qafiah import get_qafiyah
from collections import Counter
from difflib import SequenceMatcher
from pyarabic.araby import strip_tashkeel
import traceback
import sys
import gdown
from .Bohour.bohour import bohours_list
from .GPTDiacritizer import GPTDiacritizer
from .MeterClassifier import MeterClassifier

empty_analysis = {
    "diacritized": [],
    "arudi_style": [],
    "patterns_mismatches": [],
    "qafiyah": [],
    "meter": "",
    "closest_baits": [],
    "closest_patterns": [],
}


class BaitAnalysis:
    def __init__(self):
        self.BOHOUR_PATTERNS = {}
        self.BOHOUR_TAFEELAT = {}
        abs_path = "."
        for bahr_class in bohours_list:
            bahr = bahr_class()
            self.BOHOUR_PATTERNS[
                bahr_class.__name__.lower()
            ] = bahr.all_shatr_combinations_patterns
            self.BOHOUR_TAFEELAT[
                bahr_class.__name__.lower()
            ] = bahr.get_all_shatr_combinations(as_str_list=True)

        # Diacritization model
        self.diacritizer = GPTDiacritizer()

        # Meter classification model (Allam)
        self.classifier = MeterClassifier()

    def get_meter(self, baits):
        # TODO: add Allam model for classification
        meter_model = self.classifier
        labels = []
        for bait in baits:
            labels.append(meter_model.generate_meter(bait.strip()))
        return labels

    def similarity_score(self, a, b):
        return SequenceMatcher(None, a, b).ratio()

    def check_similarity(self, tf3, bahr):
        out = []

        if bahr != "نثر":
            meter = BOHOUR_NAMES[BOHOUR_NAMES_AR.index(bahr.strip())]
            for comb, tafeelat in zip(
                    self.BOHOUR_PATTERNS[meter],
                    self.BOHOUR_TAFEELAT[meter],
            ):
                prob = self.similarity_score(tf3, comb)
                out.append((comb, prob, tafeelat))
            return sorted(out, key=lambda x: x[1], reverse=True)
        else:
            # return empty results
            return [("", 0.0, "")]

    def majority_vote(self, a):
        return Counter(a).most_common()[0][0]

    def analyze(self, baits):
        diacritized_baits = []
        shatrs_arudi_styles_and_patterns = []
        patterns_mismatches = []
        closest_patterns_from_shatrs = []
        diacritized_shatrs = []
        closest_baits = []

        for i, bait in enumerate(baits):
            diacritized_bait = []
            for shatr in bait.split("#"):
                diacritized_shatr = self.diacritizer.diacritize_sentence(shatr.strip())
                diacritized_bait.append(diacritized_shatr.strip())

            # ignore empty baits
            if len(diacritized_bait) == 2:
                diacritized_shatrs += diacritized_bait
                diacritized_baits.append(" # ".join(diacritized_bait))

        if len(diacritized_baits) == 0:
            return empty_analysis

        meter = self.majority_vote(
            self.get_meter(diacritized_baits)
        )
        qafiyah = self.majority_vote(
            get_qafiyah(diacritized_baits)
        )

        for i, diacritized_shatr in enumerate(diacritized_shatrs):
            if len(diacritized_shatr) > 0:
                ((shatr_arudi_style, shatr_pattern),) = get_arudi_style(
                    diacritized_shatr
                )
                (closest_pattern, ratio, tafeelat) = self.check_similarity(
                    tf3=shatr_pattern,
                    bahr=meter,
                )[0]
                pattern_mismatch = find_mismatch(
                    closest_pattern,
                    shatr_pattern,
                    highlight_output=False,
                )

                closest_patterns_from_shatrs.append((closest_pattern, ratio, tafeelat))
                shatrs_arudi_styles_and_patterns.append(
                    (shatr_arudi_style, shatr_pattern)
                )
                patterns_mismatches.append(pattern_mismatch)

        analysis = {
            "diacritized": diacritized_baits,
            "arudi_style": shatrs_arudi_styles_and_patterns,
            "patterns_mismatches": patterns_mismatches,
            "qafiyah": qafiyah,
            "meter": meter,
            "closest_baits": closest_baits,
            "closest_patterns": closest_patterns_from_shatrs,
        }
        return analysis
