from w3lib.html import remove_tags
import json


def strip_html(text, remove=(), keep=()):
    """
    Remove HTML Tags only.

    `remove` and `keep` are both tuples, there are four cases:

    ==============  ============= ==========================================
    ``remove``  ``keep``          what it does
    ==============  ============= ==========================================
    **not empty**   empty         remove all tags in ``remove``
    empty           **not empty** remove all tags except the ones in ``keep``
    empty           empty         remove all tags
    **not empty**   **not empty** not allowed
    ==============  ============= ==========================================


    Remove all tags:

    >> doc = '<div><p><b>This is a link:</b> <a href="http://www.example.com">example</a></p></div>'
    >> strip_html(doc)
    u'This is a link: example'
    >>

    Keep only some tags:

    >> strip_html(doc, keep=('div',))
    u'<div>This is a link: example</div>'
    >>

    Remove only specific tags:

    >> strip_html(doc, remove=('a','b'))
    u'<div><p>This is a link: example</p></div>'
    >>

    You can't remove some and keep some:

    :param text: string
    :param remove: tuple
    :param keep: tuple
    :return: string
    """

    # this is supposed to hide users from having to know other library. For other needs such as removing certain tags
    # or keeping certain tags. Please use w3lib.html remove_tags directly
    return remove_tags(text = text, which_ones = remove ,keep = keep)


def prepare_data(data) -> str:
    """
    :param data: string,int,float,
    :return: cleaned and ready to send string to pipeline
    """
    # if list
    if isinstance(data, str):
        pass
    elif isinstance(data, int):
        data = str(data)
    elif isinstance(data, float):
        data = str(data)
    elif isinstance(data, list):
        data = ' | '.join(data)
    elif isinstance(data, dict):
        data = json.dumps(data)
    elif isinstance(data, bytes):
        data = data.decode('utf-8')
    else:
        data = str(data)

    data = data.strip()

    return data
