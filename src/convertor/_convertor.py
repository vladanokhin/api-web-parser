from xmljson import Cobra
from xml.etree.ElementTree import fromstring, ParseError
from typing import List, Any, Optional, OrderedDict, Dict

from configs import AppConfig


class Convertor:
    """
    Class for converting from xml to md
    """

    def __init__(self) -> None:
        self.cfg = AppConfig()
        self.cobra = Cobra(dict_type=dict, invalid_tags='drop')

    def remove_attributes(self, xml_element: List[Dict[str, Any]]) -> None:
        for i, element in enumerate(xml_element):
            if isinstance(element, dict):
                for sub_key, sub_value in element.items():
                    if isinstance(sub_value, dict) and sub_value.__len__() == 2:
                        keys = list(sub_value.keys())
                        if 'children' in keys:
                            keys.remove('children')
                            key = keys[0]
                            xml_element[i] = {key: sub_value['children']}
                    if isinstance(sub_value, list):
                        self.remove_attributes(xml_element=sub_value)

    @staticmethod
    def replace_headers(elements: List[str], title: str) -> List[str]:
        for i, element in enumerate(elements):
            elements[i] = element.replace('#', '##')
        if elements[0].startswith('##'):
            elements[0] = elements[0].replace('##', '#')
        else:
            elements.insert(0, f'# {title}')
        return elements

    def search_elements(self, xml_element: list, title: str = None, min_len: int = 5) -> Optional[str]:
        text = []
        for element in xml_element:
            if isinstance(element, dict):
                for subelement_type, subelement_text in element.items():
                    if str(subelement_text).strip() == '' or str(subelement_text).strip().startswith('{'):
                        continue
                    if isinstance(subelement_type, OrderedDict):
                        subelement_type, subelement_text = subelement_text['children'].items()

                    if subelement_type == 'head':
                        text.append(f'# {subelement_text}\n')

                    if subelement_type == 'p':
                        text.append(f'\n{subelement_text}\n\n')

                    if subelement_type == 'quote':
                        text.append(f'\n*{subelement_text}*\n\n')

                    if subelement_type == 'list':
                        if 'children' in subelement_text:
                            for list_item in subelement_text['children']:
                                for list_sub_item in list_item.values():
                                    if str(list_sub_item).strip() != '':
                                        text.append(f"* {list_sub_item}")
        if len(text) <= min_len:
            return None
        text = self.replace_headers(elements=text, title=title)
        return ''.join(text)

    @staticmethod
    def get_attribute(data: dict, attribute_name: str) -> str:
        try:
            attr: str = data['doc']['attributes'][attribute_name]
        except KeyError:
            attr = ''
        return attr

    def convert(self, xml_text: str) -> Optional[str]:
        """
        Conver xml text to md
        :param xml_text: xml text
        :return: md text or None
        """
        xml_content = xml_text
        xml_content = xml_content.replace("<div>", "").replace("</div>", "")

        try:
            data = self.cobra.data(fromstring(xml_content))
        except ParseError:
            return None

        title: str = self.get_attribute(data=data, attribute_name='title')

        try:
            root = data['doc']['children'][0]['main']['children']
        except TypeError:
            return None

        self.remove_attributes(xml_element=root)
        text = self.search_elements(xml_element=root, title=title, min_len=1)

        return text
