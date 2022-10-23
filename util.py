def split_list(orignal_list: []):
    """
    split list into 2 dimension list with every 2 elements sublist
    """
    res = []
    for index in range(0, len(orignal_list)-1):
        res.append((orignal_list[index], orignal_list[index+1]))
    return res

