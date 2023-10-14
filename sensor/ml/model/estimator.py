class TargetValueMapping:
    def __init__(self):
        self.neg: int = 0
        self.pos: int = 1

    def to_dict(self):
        return self.__dict__

    def reverse_mapping(self):
        mapping_respone = self.to_dict()
        return dict(zip(mapping_respone.values(), mapping_respone.keys()))
    
class SensorModel:

    def __init__(self, preprocessor, model):
        try:
            self.preprocessor = preprocessor
            self.model = model
        except Exception as e:
            raise e
    
    def predict(self, data):
        try:
            data_transform = self.preprocessor.transform(data)
            y_hat = self.model.predict(data_transform)
            return y_hat
        except Exception as e:
            raise e