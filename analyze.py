import requests


def analyse(sentence):
    pre_process_node = 'http://7410e27a.ngrok.io/pre-process'
    hate_level_node = 'http://b2a7e027.ngrok.io/hate-detection'
    category_node = 'http://48733011.ngrok.io/domain-detection'

    try:
        pre_process_request = requests.post(pre_process_node + '?sentence=' + sentence)
        pre_process_request.raise_for_status()
        pre_process_response = (pre_process_request.content.decode('unicode-escape').replace('[', '').replace(']', '').replace('"', '').split(","))

        sent_array = []
        for sent in pre_process_response:
            sent_array.append(sent)
            # print(sent)

        payload = {"sentence": sent_array}
        hate_level_request = requests.post(hate_level_node, json=payload)
        hate_level_request.raise_for_status()
        hate_level_response = hate_level_request.text.replace('[', '').replace(']', '').replace('"', '').split(",")

        category_request = requests.post(category_node, json=payload)
        category_request.raise_for_status()
        category_response = category_request.text

        # print(type(hate_level_response))
        # print(hate_level_response)
        # print(category_response)

        return hate_level_response[0].strip(), hate_level_response[1].strip(), category_response.strip()

    except requests.exceptions.HTTPError as err:
        print(err)