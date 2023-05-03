from fasttext import load_model


THRESHOLD_DEFAULT = 0.7


def get_label_text(label):
    label_sub = '__label__'
    return label.replace(label_sub, '')


class SpeechProcessor:
    def __init__(self, model_file, process_threshold=THRESHOLD_DEFAULT):
        """Class responsible for speech categorizations and predictions.
        
        :Parameters:
            - `model_file`: String. Relative path to Fasttext model file.
            - `process_threshold`: Float. Threshold for model prediction acceptance.
        """
        self._model = load_model(model_file)
        self._process_treshold = process_threshold

    def process(self, question):
        """Function to process question against the model.
        
        :Parameters:
            - `question`: String. Question to process.
        """
        result = None
        labels, probs = self._model.predict(question)        
        biggest_prob = max(probs)
        # Check if biggest probability is above the threshold.
        if biggest_prob > self._process_treshold:
            # Get label for biggest probability.
            most_probable_label = labels[list(probs).index(biggest_prob)]
            # Strip any metadata from label.
            result = get_label_text(most_probable_label)    
        return result