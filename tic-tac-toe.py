playing_field = """
		-------------
		| 1 | 2 | 3 |
		-------------
		| 4 | 5 | 6 |
		-------------
		| 7 | 8 | 9 |
		-------------
			   """

numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
indices = [playing_field.index(number) for number in numbers]

patterns_to_check = [[indices[0],indices[1],indices[2]]
					,[indices[3],indices[4],indices[5]]
					,[indices[6],indices[7],indices[8]]
					,[indices[0],indices[3],indices[6]]
					,[indices[1],indices[4],indices[7]]
					,[indices[2],indices[5],indices[8]]
					,[indices[0],indices[4],indices[8]]
					,[indices[2],indices[4],indices[6]]]

def get_player_name(player):
    player_name = raw_input("What is the name of "+player+"? ")
    while player_name == "":
        player_name = raw_input("I need a name for pete's sake! What is the name of "+player+"? ")
    return player_name

def check_names(name_1, name_2):
    while name_1 == name_2:
        name_2 = raw_input("The two names are identical. "
						   "Player 2 will need to choose a new name. ")
    return name_2

def get_and_process_player_choice(player, token, string):
    choice = raw_input(player + ", what number do you want to place your "+token+" on? ")
    while choice not in string or not [number for number in numbers if number == choice]:
        choice = raw_input("That's not a valid choice. Choose an integer from 1 through 9 that has not been chosen yet. ")
    else:
        new_string = string.replace(str(choice), token)
    return new_string

def check_pattern(string, pattern):
    list = [string[element] for element in pattern]
    return len(set(list)) == 1

def check_all_patterns(string, all_patterns):
    list = [check_pattern(string, pattern) for pattern in all_patterns]
    return True in list

if __name__ == "__main__":
    player_x = get_player_name('player 1')
    player_o = get_player_name('player 2')
    player_o = check_names(player_x, player_o)
    print playing_field
    i = 0
    check_function = False
    while i < 9 and not check_function:
        if i%2 == 0:
            playing_field = get_and_process_player_choice(player_x, 'X', playing_field)
            print playing_field
        else:
            playing_field = get_and_process_player_choice(player_o, 'O', playing_field)
            print playing_field
        check_function = check_all_patterns(playing_field, patterns_to_check)
        if check_function == True:
            if i%2 == 0:
                print(player_x+" wins!")
            else:
                print(player_o+" wins!")
        i += 1