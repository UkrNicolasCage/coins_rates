def change( old_list: list, new_val):
    if new_val in old_list:
        return old_list
    else:
        if len(old_list) == 4:
            old_list.insert(0, new_val)
            new_list = old_list[:-1]
            return new_list
        else:
            old_list.insert(0, new_val)
            return old_list
 
