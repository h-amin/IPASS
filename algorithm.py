import csv
import psycopg2

# User input statement.
while True:
    try:
        primary_question = input("Type the name of your desired main plant: ")
    except ValueError:
        print("Sorry, I did not understand that.")
        continue
    else:
        break


# Establishing database access.
def get_sql_connection(psycopg2):
    connection = psycopg2.connect(user="postgres",
                                  password="38gAc57ip!",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="IPASS")
    return connection


# Opening the database connection
def open_db_connection():
    global connection, cursor
    try:
        connection = get_sql_connection(psycopg2)
        cursor = connection.cursor()
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)


# Closing the database connection
def close_db_connection():
    if connection:
        connection.commit()
        cursor.close()
        connection.close()


# SQL statement function that will create a table, provided the table doesn't exist beforehand.
def create_table_plant_data():
    create_table = "CREATE TABLE IF NOT EXISTS plant_data (" \
                   "plant_name varchar PRIMARY KEY," \
                   "type varchar, " \
                   "water varchar, " \
                   "bloom_time varchar, " \
                   "soil varchar," \
                   "sunlight varchar, " \
                   "nutrient_bestowement varchar, " \
                   "toxicity varchar)"
    cursor.execute(create_table)


# SQL statement function that will insert the plants_data.csv file into the created table.
def insert_csv_data():
    # ! IMPORTANT ! --> Change this to the path where you have placed the plants.csv file.
    with open('C:/Users/hamed/Documents/plants_data.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            cursor.execute(
                "INSERT INTO plant_data VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", row)


# Small SQL-query to extract and retrieve all plant_names within the database
def lst_plant_names():
    open_db_connection()
    cursor.execute("SELECT DISTINCT plant_name FROM plant_data;")
    name_data = cursor.fetchall()
    close_db_connection()
    return name_data


def main_characteristics():
    """
    The main_characteristics function simply shows us the attributes of the prompted PRIMARY plant.
    It searches for key attributes and extracts the data through a simple SQL query, so in turn we get a list with
    the necessary information.
    """
    plant_names = lst_plant_names()
    plant_names_lst = []
    result_lst = []

    # Removing redundant parentheses and unused clutter.
    [plant_names_lst.append(i[0]) for i in plant_names]

    if primary_question in plant_names_lst:
        open_db_connection()
        # Extracting the necessary attribute data in order to manipulate it afterwards.
        cursor.execute("SELECT "
                       "type, "
                       "water, "
                       "soil, "
                       "sunlight, "
                       "nutrient_bestowement, "
                       "toxicity, "
                       "bloom_time "
                       "FROM plant_data WHERE plant_name = '{0}'".format(primary_question))
        result = cursor.fetchone()
        close_db_connection()
        result_lst.append(result)

    return result_lst


def recommendations():
    """
    The "Ideal" recommendation is a plant with the weighted sum of plant attributes that comes closest
    to the sum of plant_characteristics. (which is 150 total) The essence of this function is to reveal the plants that
    have the highest weighted value that correlates to the PRIMARY plant, in order to create a sorted list which
    in turn will allow us to see which plants are most suitable for recommendation.
    """

    plant_characteristics = main_characteristics()
    weight_lst = []

    # Appointed weights to each attribute value that has been obtained from the afore mentioned main_characteristics.
    p_type_weight = 5
    p_water_weight = 20
    p_soil_weight = 20
    p_sunlight_weight = 20
    p_bestowement_weight = 30
    p_toxicity_weight = 40
    p_bloom_weight = 5

    weight_lst.extend((p_type_weight, p_water_weight, p_soil_weight, p_sunlight_weight, p_bestowement_weight,
                       p_toxicity_weight, p_bloom_weight))

    # weight_lst.sum() --> 150

    total_sum_dict = {}

    for h in range(len(lst_plant_names())):
        sum_values = []
        sum_keys = []
        check_plant = lst_plant_names()[h][0]
        sum_values.append(check_plant)
        for i in range(len(plant_characteristics)):
            # key_lst = plant_characteristics[i]
            p_type = plant_characteristics[i][0]
            p_water_level = plant_characteristics[i][1]
            p_soil = plant_characteristics[i][2]
            p_sunlight = plant_characteristics[i][3]
            # p_bestowement = plant_characteristics[i][4]
            # p_toxicity = plant_characteristics[i][5]
            p_bloom = plant_characteristics[i][6]

            # zip_iterator = zip(key_lst, weight_lst)
            # primary_plant_dict = dict(zip_iterator)

            open_db_connection()

            '''
            For the type of plants, it is preferred NOT to have the same type of plant surrounding your primary plant.
            The way the code is currently setup is heavily depended on the format of the database. (this goes for all the other attributes)
            If there are different attribute levels to water for example, one has to change the values manually.
            '''

            cursor.execute("SELECT DISTINCT type FROM plant_data WHERE plant_name = '{0}'".format(check_plant))
            type_data = cursor.fetchall()  # Obtain data
            type_values = []
            type_keys = []
            [type_values.append(i[0]) for i in type_data]  # Remove brackets
            for type in type_values:
                if type != p_type:
                    type_weight = 5
                    type_keys.append(type_weight)
                else:
                    type_weight = 0
                    type_keys.append(type_weight)
            zip_iterator = zip(type_values, type_keys)
            type_dict = dict(zip_iterator)

            ''' 
            You primarily want the water level to be the same as your primary plant water attribute,
            should this not be the case however, most plants can live with exceeding/subsceeding amounts of water.
            '''

            cursor.execute("SELECT DISTINCT water FROM plant_data WHERE plant_name = '{0}'".format(check_plant))
            water_data = cursor.fetchall()
            water_values = []
            water_keys = []
            [water_values.append(i[0]) for i in water_data]
            for water in water_values:
                if water == p_water_level:
                    water_weight = 20
                    water_keys.append(water_weight)
                elif water == 'Average':
                    water_weight = 15
                    water_keys.append(water_weight)
                elif water == 'Low':
                    water_weight = 10
                    water_keys.append(water_weight)
                elif water == 'High':
                    water_weight = 10
                    water_keys.append(water_weight)
            zip_iterator = zip(water_values, water_keys)
            water_dict = dict(zip_iterator)

            '''
            The soil will always want to be the same as the other plant attributes, an difference in botanic habitat
            will most definitely have an impact on the development of all the plants in general.
            '''
            cursor.execute("SELECT DISTINCT soil FROM plant_data WHERE plant_name = '{0}'".format(check_plant))
            soil_data = cursor.fetchall()
            soil_values = []
            soil_keys = []
            [soil_values.append(i[0]) for i in soil_data]
            for soil in soil_values:
                if soil == p_soil:
                    soil_weight = 20
                    soil_keys.append(soil_weight)
                else:
                    soil_weight = 5
                    soil_keys.append(soil_weight)
            zip_iterator = zip(soil_values, soil_keys)
            soil_dict = dict(zip_iterator)

            '''
            For most plants, sunlight is crucial to their development, however in some cases, having an overdose of sunlight,
            or a lack of sunlight, can be suffered, as long as it doesn't reach a detrimental state.
            The general consesus states that garden plants require alot of sun, so we have implemented as such.
            '''

            cursor.execute("SELECT DISTINCT sunlight FROM plant_data WHERE plant_name = '{0}'".format(check_plant))
            sunlight_data = cursor.fetchall()
            sunlight_values = []
            sunlight_keys = []
            [sunlight_values.append(i[0]) for i in sunlight_data]
            for sunlight in sunlight_values:
                if sunlight == p_sunlight:
                    sunlight_weight = 20
                    sunlight_keys.append(sunlight_weight)
                elif sunlight == 'Full':
                    sunlight_weight = 15
                    sunlight_keys.append(sunlight_weight)
                elif sunlight == 'Average':
                    sunlight_weight = 10
                    sunlight_keys.append(sunlight_weight)
                elif sunlight == 'Low':
                    sunlight_weight = 5
                    sunlight_keys.append(sunlight_weight)
            zip_iterator = zip(sunlight_values, sunlight_keys)
            sunlight_dict = dict(zip_iterator)

            '''
            Nutrient bestowement is the second most important attribute for this algorithm, if a plant does not relinquish
            their nutrients as much as they would consume it, the primary plant will be unable to gain an optimal enviroment
            to develop.
            '''

            cursor.execute(
                "SELECT DISTINCT nutrient_bestowement FROM plant_data WHERE plant_name = '{0}'".format(check_plant))
            n_b_data = cursor.fetchall()
            n_b_values = []
            n_b_keys = []
            [n_b_values.append(i[0]) for i in n_b_data]
            for n_b in n_b_values:
                if n_b == 'Relinquish':
                    n_b_weight = 30
                    n_b_keys.append(n_b_weight)
                elif n_b == 'Receive':
                    n_b_weight = 5
                    n_b_keys.append(n_b_weight)
            zip_iterator = zip(n_b_values, n_b_keys)
            n_b_dict = dict(zip_iterator)

            '''
            Toxicity, just like nutrient bestowement is equally, if not the most important attribute of a plant that we need
            to be wary of. If a plant has too much toxicity levels, it will essentially destroy the plants surrounding it.
            (Or at the very least impact their growth and survivability.)
            It is much more preferred to isolate these toxic plants and let them develop in a enclosed enviroment.
            '''

            cursor.execute("SELECT DISTINCT toxicity FROM plant_data WHERE plant_name = '{0}'".format(check_plant))
            toxic_data = cursor.fetchall()
            toxic_values = []
            toxic_keys = []
            [toxic_values.append(i[0]) for i in toxic_data]
            for toxic in toxic_values:
                if toxic == 'High':
                    toxic_weight = 0
                    toxic_keys.append(toxic_weight)
                elif toxic == 'Medium':
                    toxic_weight = 2
                    toxic_keys.append(toxic_weight)
                elif toxic == 'Low':
                    toxic_weight = 15
                    toxic_keys.append(toxic_weight)
                elif toxic == 'None':
                    toxic_weight = 40
                    toxic_keys.append(toxic_weight)
            zip_iterator = zip(toxic_values, toxic_keys)
            toxic_dict = dict(zip_iterator)

            '''
            Bloom time is quality of life extra. It would be most efficient and enjoyable to see your garden bloom
            at around the same time. That way one can enjoy their garden to the fullest.
            '''

            cursor.execute("SELECT DISTINCT bloom_time FROM plant_data WHERE plant_name = '{0}'".format(check_plant))
            bloom_data = cursor.fetchall()
            bloom_values = []
            bloom_keys = []
            [bloom_values.append(i[0]) for i in bloom_data]
            for bloom in bloom_values:
                if bloom != p_bloom:
                    bloom_weight = 5
                    bloom_keys.append(bloom_weight)
                else:
                    bloom_weight = 0
                    bloom_keys.append(bloom_weight)
            zip_iterator = zip(bloom_values, bloom_keys)
            bloom_dict = dict(zip_iterator)

            # Collecting the sum of these attribute weights
            dict_type_sum = sum(type_dict.values())
            dict_water_sum = sum(water_dict.values())
            dict_soil_sum = sum(soil_dict.values())
            dict_sunlight_sum = sum(sunlight_dict.values())
            dict_n_b_sum = sum(n_b_dict.values())
            dict_toxicity_sum = sum(toxic_dict.values())
            dict_bloom_sum = sum(bloom_dict.values())

            total_sum = dict_type_sum + dict_water_sum + dict_soil_sum + dict_sunlight_sum + dict_n_b_sum + dict_toxicity_sum + dict_bloom_sum
            sum_keys.append(total_sum)

            close_db_connection()

        # putting the newfound key sum values and record name values in a dictionary for structure purposes
        zip_iterator = zip(sum_values, sum_keys)
        sum_dict = dict(zip_iterator)
        total_sum_dict.update(sum_dict)

    # sorting the dictionary based on the highest key value. (plant most suitable for the PRIMARY plant)
    myDict = sorted(total_sum_dict.items(), key=lambda x: x[1], reverse=True)

    recommendations_lst = []

    for j in range(len(myDict)):
        recommendations_lst.append(myDict[j][0])

    if primary_question in recommendations_lst:
        recommendations_lst.remove(primary_question)

    top_4 = recommendations_lst[:4]

    return top_4


def secondary_recommendations():
    """
    This function bases itself off the results of function: recommendations(). The code will take the initial Primary
    question, and find the highest key valued plant_name within the sorted list, and return it so that the same process
    can be used to ascertain what the top_3 most suitable plant combinations are for that specific recommended plant.
    """

    secondary_start = recommendations()[:1]

    result_lst = []

    open_db_connection()
    cursor.execute("SELECT "
                   "type, "
                   "water, "
                   "soil, "
                   "sunlight, "
                   "nutrient_bestowement, "
                   "toxicity, "
                   "bloom_time "
                   "FROM plant_data WHERE plant_name = '{0}'".format(secondary_start[0]))
    result = cursor.fetchone()
    close_db_connection()
    result_lst.append(result)

    weight_lst = []

    s_type_weight = 5
    s_water_weight = 20
    s_soil_weight = 20
    s_sunlight_weight = 20
    s_bestowement_weight = 30
    s_toxicity_weight = 40
    s_bloom_weight = 5

    weight_lst.extend((s_type_weight, s_water_weight, s_soil_weight, s_sunlight_weight, s_bestowement_weight,
                       s_toxicity_weight, s_bloom_weight))

    # weight_lst.sum() = 150

    total_sum_dict = {}

    for h in range(len(lst_plant_names())):
        sum_values = []
        sum_keys = []
        check_plant = lst_plant_names()[h][0]
        sum_values.append(check_plant)
        for i in range(len(result_lst)):
            s_type = result_lst[i][0]
            s_water_level = result_lst[i][1]
            s_soil = result_lst[i][2]
            s_sunlight = result_lst[i][3]
            s_bloom = result_lst[i][6]

            open_db_connection()

            '''
            For the type of plants, it is preferred NOT to have the same type of plant surrounding your primary plant.
            The way the code is currently setup is heavily depended on the format of the database. (this goes for all the other attributes)
            If there are different attribute levels to water for example, one has to change the values manually.
            '''

            cursor.execute("SELECT DISTINCT type FROM plant_data WHERE plant_name = '{0}'".format(check_plant))
            type_data = cursor.fetchall()
            type_values = []
            type_keys = []
            [type_values.append(i[0]) for i in type_data]
            for type in type_values:
                if type != s_type:
                    type_weight = 5
                    type_keys.append(type_weight)
                else:
                    type_weight = 0
                    type_keys.append(type_weight)
            zip_iterator = zip(type_values, type_keys)
            type_dict = dict(zip_iterator)
            # print(type_dict)

            ''' 
            You primarily want the water level to be the same as your primary plant water attribute,
            should this not be the case however, most plants can live with exceeding/subsceeding amounts of water.
            '''

            cursor.execute("SELECT DISTINCT water FROM plant_data WHERE plant_name = '{0}'".format(check_plant))
            water_data = cursor.fetchall()
            water_values = []
            water_keys = []
            [water_values.append(i[0]) for i in water_data]
            for water in water_values:
                if water == s_water_level:
                    water_weight = 20
                    water_keys.append(water_weight)
                elif water == 'Average':
                    water_weight = 15
                    water_keys.append(water_weight)
                elif water == 'Low':
                    water_weight = 10
                    water_keys.append(water_weight)
                elif water == 'High':
                    water_weight = 10
                    water_keys.append(water_weight)
            zip_iterator = zip(water_values, water_keys)
            water_dict = dict(zip_iterator)

            '''
            The soil will always want to be the same as the other plant attributes, an difference in botanic habitat
            will most definitely have an impact on the development of all the plants in general.
            '''

            cursor.execute("SELECT DISTINCT soil FROM plant_data WHERE plant_name = '{0}'".format(check_plant))
            soil_data = cursor.fetchall()
            soil_values = []
            soil_keys = []
            [soil_values.append(i[0]) for i in soil_data]
            for soil in soil_values:
                if soil == s_soil:
                    soil_weight = 20
                    soil_keys.append(soil_weight)
                else:
                    soil_weight = 5
                    soil_keys.append(soil_weight)
            zip_iterator = zip(soil_values, soil_keys)
            soil_dict = dict(zip_iterator)

            '''
            For most plants, sunlight is crucial to their development, however in some cases, having an overdose of sunlight,
            or a lack of sunlight, can be suffered, as long as it doesn't reach a detrimental state.
            The general consesus states that garden plants require alot of sun, so we have implemented as such.
            '''

            cursor.execute("SELECT DISTINCT sunlight FROM plant_data WHERE plant_name = '{0}'".format(check_plant))
            sunlight_data = cursor.fetchall()
            sunlight_values = []
            sunlight_keys = []
            [sunlight_values.append(i[0]) for i in sunlight_data]
            for sunlight in sunlight_values:
                if sunlight == s_sunlight:
                    sunlight_weight = 20
                    sunlight_keys.append(sunlight_weight)
                elif sunlight == 'Full':
                    sunlight_weight = 15
                    sunlight_keys.append(sunlight_weight)
                elif sunlight == 'Average':
                    sunlight_weight = 10
                    sunlight_keys.append(sunlight_weight)
                elif sunlight == 'Low':
                    sunlight_weight = 5
                    sunlight_keys.append(sunlight_weight)
            zip_iterator = zip(sunlight_values, sunlight_keys)
            sunlight_dict = dict(zip_iterator)

            '''
            Nutrient bestowement is the second most important attribute for this algorithm, if a plant does not relinquish
            their nutrients as much as they would consume it, the primary plant will be unable to gain an optimal enviroment
            to develop.
            '''

            cursor.execute(
                "SELECT DISTINCT nutrient_bestowement FROM plant_data WHERE plant_name = '{0}'".format(check_plant))
            n_b_data = cursor.fetchall()
            n_b_values = []
            n_b_keys = []
            [n_b_values.append(i[0]) for i in n_b_data]
            for n_b in n_b_values:
                if n_b == 'Relinquish':
                    n_b_weight = 30
                    n_b_keys.append(n_b_weight)
                elif n_b == 'Receive':
                    n_b_weight = 5
                    n_b_keys.append(n_b_weight)
            zip_iterator = zip(n_b_values, n_b_keys)
            n_b_dict = dict(zip_iterator)

            '''
            Toxicity, just like nutrient bestowement is equally, if not the most important attribute of a plant that we need
            to be wary of. If a plant has too much toxicity levels, it will essentially destroy the plants surrounding it.
            (Or at the very least impact their growth and survivability.)
            It is much more preferred to isolate these toxic plants and let them develop in a enclosed enviroment.
            '''

            cursor.execute("SELECT DISTINCT toxicity FROM plant_data WHERE plant_name = '{0}'".format(check_plant))
            toxic_data = cursor.fetchall()
            toxic_values = []
            toxic_keys = []
            [toxic_values.append(i[0]) for i in toxic_data]
            for toxic in toxic_values:
                if toxic == 'High':
                    toxic_weight = 0
                    toxic_keys.append(toxic_weight)
                elif toxic == 'Medium':
                    toxic_weight = 2
                    toxic_keys.append(toxic_weight)
                elif toxic == 'Low':
                    toxic_weight = 15
                    toxic_keys.append(toxic_weight)
                elif toxic == 'None':
                    toxic_weight = 40
                    toxic_keys.append(toxic_weight)
            zip_iterator = zip(toxic_values, toxic_keys)
            toxic_dict = dict(zip_iterator)

            '''
            Bloom time is quality of life extra. It would be most efficient and enjoyable to see your garden bloom
            at around the same time. That way one can enjoy their garden to the fullest.
            '''

            cursor.execute("SELECT DISTINCT bloom_time FROM plant_data WHERE plant_name = '{0}'".format(check_plant))
            bloom_data = cursor.fetchall()
            bloom_values = []
            bloom_keys = []
            [bloom_values.append(i[0]) for i in bloom_data]
            for bloom in bloom_values:
                if bloom == s_bloom:
                    bloom_weight = 5
                    bloom_keys.append(bloom_weight)
                else:
                    bloom_weight = 0
                    bloom_keys.append(bloom_weight)
            zip_iterator = zip(bloom_values, bloom_keys)
            bloom_dict = dict(zip_iterator)

            dict_type_sum = sum(type_dict.values())
            dict_water_sum = sum(water_dict.values())
            dict_soil_sum = sum(soil_dict.values())
            dict_sunlight_sum = sum(sunlight_dict.values())
            dict_n_b_sum = sum(n_b_dict.values())
            dict_toxicity_sum = sum(toxic_dict.values())
            dict_bloom_sum = sum(bloom_dict.values())

            total_sum = dict_type_sum + dict_water_sum + dict_soil_sum + dict_sunlight_sum + dict_n_b_sum + dict_toxicity_sum + dict_bloom_sum
            sum_keys.append(total_sum)

            close_db_connection()

        zip_iterator = zip(sum_values, sum_keys)
        sum_dict = dict(zip_iterator)
        total_sum_dict.update(sum_dict)
    myDict = sorted(total_sum_dict.items(), key=lambda x: x[1], reverse=True)

    recommendations_lst = []

    top_4 = recommendations()[:4]

    for j in range(len(myDict)):
        recommendations_lst.append(myDict[j][0])

    for y in range(len(top_4)):
        if top_4[y] in recommendations_lst:
            recommendations_lst.remove(top_4[y])
        elif primary_question in recommendations_lst:
            recommendations_lst.remove(primary_question)
        elif secondary_start in recommendations_lst:
            recommendations_lst.remove(secondary_start)

    top_3 = recommendations_lst[:3]
    return top_3


def add_recommendations_column():
    """
    Function to create two extra columns by the name of primary and secondary recommendations, seen as how
    the initial create_table function did not include these columns. This is done consciously, as the csv.file does not
    have a recommendation column as one would expect from a mock botanical database.
    """
    open_db_connection()
    add_column = "ALTER TABLE plant_data ADD primary_recommendations varchar"
    cursor.execute(add_column)
    add_column = "ALTER TABLE plant_data ADD secondary_recommendations varchar"
    cursor.execute(add_column)
    close_db_connection()


def fill_recommendations_column():
    """
    This function will allow the top 4 plants that have been identified with usage of the recommendations() function,
    to be saved within the data under the primary_recommendations tab. The function will work for every plant that the
    user decides to fill when prompted.
    """
    top_4 = recommendations()
    p_first_string = top_4[0]
    p_second_string = top_4[1]
    p_third_string = top_4[2]
    p_fourth_string = top_4[3]
    p_full_string = p_first_string + ', ' + p_second_string + ', ' + p_third_string + ', ' + p_fourth_string

    top_3 = secondary_recommendations()
    s_first_string = top_3[0]
    s_second_string = top_3[1]
    s_third_string = top_3[2]
    s_full_string = s_first_string + ', ' + s_second_string + ', ' + s_third_string

    try:
        open_db_connection()
        query = "UPDATE plant_data " \
                "SET primary_recommendations = '{0}'," \
                "secondary_recommendations = '{1}'" \
                "WHERE plant_name = '{2}'".format(p_full_string, s_full_string, primary_question)
        cursor.execute(query)
        print('SUCCES. the recommendations have been inserted for the plant', primary_question)
        close_db_connection()
    except ValueError:
        print('ERROR. database is unable to retrieve the recommendations')
        print('The primary recommendations are: ', p_full_string)
        print('The secondary recommendations are: ', s_full_string)


# Function to establish and create the database as well as fill in the csv.file into the designated columns/rows.
def fill_table():
    open_db_connection()
    create_table_plant_data()
    insert_csv_data()
    close_db_connection()
