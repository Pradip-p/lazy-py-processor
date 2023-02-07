import re


def domToArray(domElements, text_type="TEXT", ignoreBlank=True, keyType=None):
    """
        Parse HTML dom and returns dictionary of data with key value

        There are four cases to parse the dom:

        case 1: if text_type is TEXT, it returns objects with all text in dom elements
        case 2: if text_type is TEXT_URL, it returns dictionary of text and url. Example
            >> if elements are <a href= "hello.com">Hello</a> then it returns {text: Hello,url:"hello.com"}
        case 3: if text_type is TEXT_VALUE, it returns dictionary of text and value. Example
            >> if elements are <option value="1"> ONE </option> then it returns {text:ONE,value:1}
        case Final:
            >> if none of text_type matches then we parse elements depending on its attributes i.e. class or value etc.
               and returns value is quite different comparing above 3 cases:
                > Here, we return data depending in keyType. i.e. if keyType is TEXT or CLASS or ATTR_VALUE then we modify key
                  with its value and return dictionary.
                For Example: if we call domToArray(elements,"ATTR_VALUE",'',"TEXT") then our function returns
                {ONE:1,TWO:2}. here we made options value dictionary key and text a dictionary value.

    """
    data = []
    count = len(domElements)
    if count:
        for dom in domElements:
            if text_type == "TEXT":
                text = dom.xpath('text()').get(default='').strip()
                if text != '' or ignoreBlank == False:
                    data.append(text)
            elif text_type == "TEXT_URL":
                textUrl = {'text': dom.xpath('text()').get(), 'url': dom.xpath('@href').get(default='')}
                data.append(textUrl)
            elif text_type == "TEXT_VALUE":
                textValue = {'text': dom.xpath('text()').get(default=''), 'value': dom.xpath('@value').get(default='')}
                data.append(textValue)
            else:
                if re.search("^ATTR_(.*)", text_type):
                    split = text_type.split("_")
                    to_lower = str.lower(split[1])
                    if dom.xpath('@' + to_lower).get() != '':
                        if keyType == "TEXT":
                            key = dom.xpath('text()').get()
                            keyValue = {key: dom.xpath('@' + to_lower).get()}
                            data.append(keyValue)
                        elif keyType == "CLASS":
                            key = dom.xpath('@class').get()
                            keyValue = {key: dom.xpath('@' + to_lower).get()}
                            data.append(keyValue)
                        else:
                            text = dom.xpath('@' + to_lower).get(default='')
                            data.append(text)

    return data
