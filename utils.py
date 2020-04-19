
def check_password_hash(hash,password):
    if hash == password:
        return True
    else:
        return False
def get_cards_summary_model():
    data = dict()
    data["used_on_amazon"] = 0
    data['used_on_google'] = 0
    data['total_used'] = 0
    data['expired'] = 0
    data['total'] = 0
    data['in_progress'] = 0
    return data
def getcards_trim_data(cards):
    # result = []
    # for card in cards:
    #     temp = dict()
    #     temp['Id'] = card.id
    #     temp['Name'] = card.card_name
    #     temp['Card Number'] = card.card_number
    #     temp['Month'] = card.month
    #     temp['Year'] = card.year
    #     temp['Address'] = card.address
    #     result.append(temp)
    result = []
    for card in cards:
        temp = []
        temp.append(card.id)
        temp.append(card.card_name)
        temp.append(card.card_number)
        temp.append(card.month)
        temp.append(card.year)
        temp.append(card.cvv)
        temp.append(card.address)
        result.append(temp)
    return result
