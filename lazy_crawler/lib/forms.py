def get_form_fields(selector, response, selector_type='xpath', excluded_fields=[], allowed_fields=[]):
    """
    Returns a dictionary of all input fields and their values of the form with the present values

    :param selector:  Selector
    :param selector_type: selector type  Options:
                                                css or xpath
    :param response: scrapy response of the url
    :param excluded_fields: list of fields to exclude. Default no field will be excluded
    :param allowed_fields: list of fields to allow. Only the fields in this list will be returned. Default all fields
                            returned
    :return: a dictionary of input name and values

    Tested on :
        https://prixatech.com/contact-us/
        https://hamrobazaar.com/register.php
        https://www.outbrain.com/contact/
        https://www.atlassian.com/company/contact/contact-ceos
        http://www.echoecho.com/htmlforms09.htm
        https://www.w3schools.com/tags/tryit.asp?filename=tryhtml_input_checked
        https://www.w3schools.com/tags/tryit.asp?filename=tryhtml5_input_type_radio
        https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/radio
        http://www.echoecho.com/htmlforms10.htm
        Checked for multiple inputs too
    """
    fields = {}  # defining a empty dictionary to store form field name as keys and value as value
    if selector_type == 'xpath':
        form_data = response.xpath(selector)
    else:
        form_data = response.css(selector)
    for input_ in form_data.xpath('.//input'):
        name = input_.xpath('@name').get(default='')
        if name not in excluded_fields:  # checking if name has been requested to exclude form the form
            if len(allowed_fields) == 0:
                pass
            elif name not in allowed_fields:
                # if allowed fields is defined and our name is not present in allowed_fields then skip the name
                continue
            # form field extraction logic here
            # value = input_.xpath('@value').get(default='')
            # checking if the input_ values are checkboxes or radio button.
            if input_.xpath('@type').get(default='') == 'checkbox' or input_.xpath('@type').get(default='') == 'radio':
                if input_.xpath('@checked').get(default='') == 'checked':
                    fields[name] = input_.xpath('@value').get(default='')
                    if fields[name] == '':
                        fields[name] = 'on'
            else:  # if input_ type is not checkbox or radio button. We will directly get name and values
                fields[name] = input_.xpath('@value').get(default='')
    # select doesn't start with input so we will do it separately
    select_list = form_data.xpath('.//select')
    for select in select_list:
        options = select.xpath('.//option[@selected="selected"]')
        if len(options) == 0:  # if no option is selected by default
            fields[select.xpath('@name').get(default='')] = select.xpath('(.//options)[1]/@value').get(default='')
        elif len(options) == 1: # if only one option is selected
            if options.xpath('@value').get(default='') != '':
                fields[select.xpath('@name').get(default='')] = options.xpath('@value').get(default='')
            else:
                fields[select.xpath('@name').get(default='')] = options.xpath('.//text()').get(default='')
        else:  # if multiple options are selected
            all_options = []
            for opt in options:
                val = opt.xpath('@value').get(default='')
                if val == '':
                    val = opt.xpath('.//text()').get(default='')
                all_options.append(val)
            fields[select.xpath('@name').get(default='') + '[]'] = all_options
    return fields
