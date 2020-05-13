from calendar import timegm
from datetime import datetime


class Records:
    elements = []

    def __init__(self):
        self.elements = []

    def add(self, element: dict):
        element['performed_at'] = timegm(datetime.utcnow().utctimetuple())
        self.elements.append(element)

    def output(self):
        return self.elements

    def output_as_dict(self, key: str):
        return {
            key: self.elements
        }
