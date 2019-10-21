import numpy as np
from numpy import genfromtxt
import json



def init(user_id):

    users = user_data()
    day = movie_data('context_day.csv')
    place = movie_data('context_place.csv')

    sim = similar_users(users, user_id)
    ratings_movies = get_ratings(sim, users, user_id)

    recommended_movies = recommendation(ratings_movies, 3, day, place, ['Sun', 'Sat'], ['h'])

    movie_ratings = {}
    for i in ratings_movies:
        movie_ratings["Movie " + str(i)] = ratings_movies[i]


    recommended_movie = next(iter(recommended_movies))

    result = {
        "user": user_id,
        "1": movie_ratings,
        "2": recommended_movies,
    }

    with open('User4Result.json', 'w') as file:
        json.dump(result, file)
    file.close()
    print("File .json created")


def user_data():

    data = genfromtxt('data.csv', delimiter=', ', dtype=str)
    row = data.shape[0]
    users = {}

    for i in range(row - 1):
        current_data = data[i + 1][1:]
        for j in range(current_data.shape[0]):
            if int(current_data[j]) == -1:
                current_data[j] = 0
        users[i + 1] = np.array(current_data, dtype=int)

    return users


def movie_data(file_name):

    data = genfromtxt(file_name, delimiter=', ', dtype=str)
    row = data.shape[0]
    column = data.shape[1]
    movies = {}

    for i in range(row - 1):
        for j in range(column - 1):
            if data[i + 1][j + 1] != '-1':
                if (j+1) in movies:
                    movies[j+1] = np.append(movies[j+1], data[i+1][j+1])
                else:
                    movies[j+1] = np.array([data[i+1][j+1]])

    return movies



def similar_users(users, selected_user_id):

    knn = 4
    sim_data = {}
    for current_id in users:
        if current_id != selected_user_id:
            comp = np.array([])
            sq_current = np.array([])
            sq_selected = np.array([])
            for movie in range(users[current_id].shape[0]):
                if users[current_id][movie] > 0 and users[selected_user_id][movie] > 0:
                    comp = np.append(comp, users[current_id][movie]*users[selected_user_id][movie])
                    sq_current = np.append(sq_current, users[current_id][movie] ** 2)
                    sq_selected = np.append(sq_selected, users[selected_user_id][movie] ** 2)
            comp = np.sum(comp)
            sq_current = np.sum(sq_current) ** 0.5
            sq_selected = np.sum(sq_selected) ** 0.5
            metric = (sq_current * sq_selected)
            metric = comp / metric
            sim_data[current_id] = metric
    sim_data = sorted(sim_data.items(), key=lambda item: -item[1])
    return sim_data[:knn]


def get_avg(current_list):
    list_sum = 0
    count = 0
    for i in range(len(current_list)):
        if current_list[i] != 0:
            list_sum += current_list[i]
            count += 1
    return list_sum / count


def get_ratings(sim_users, users, selected_user):

    result_ratings = {}
    selected_user_data = users[selected_user]
    avg_rating_selected_user = get_avg(selected_user_data)

    for movie_id in range(len(selected_user_data)):
        movie_rating = selected_user_data[movie_id]
        if movie_rating == 0:
            dividend = np.array([])
            divider = np.array([])
            for user in sim_users:
                current_user_id = user[0]
                current_user_data = users[current_user_id]
                if current_user_data[movie_id] > 0:
                    avg_rating_current_user = get_avg(current_user_data)
                    dividend = np.append(dividend, user[1] * (current_user_data[movie_id] - avg_rating_current_user))
                    divider = np.append(divider, user[1])
            dividend = np.sum(dividend)
            divider = np.sum(divider)
            result_rating = avg_rating_selected_user + (dividend/divider)
            result_ratings[movie_id+1] = round(result_rating, 3)

    return result_ratings


def recommendation(movies, border_rating, context_day_data, context_place_data, current_context_day, current_context_place):

    best_movies = {}

    for i in movies:
        if movies[i] >= border_rating:
            context_day = context_day_data[i]
            context_place = context_place_data[i]
            context_day_rating = 0
            context_place_rating = 0
            for j in range(len(context_day)):
                if any(x == context_day[j] for x in current_context_day):
                    context_day_rating += 1
            for k in range(len(context_place)):
                if any(x == context_place[k] for x in current_context_place):
                    context_place_rating += 1
            best_movies[i] = (context_day_rating / len(context_day)) * (context_place_rating / len(context_place))

    max_rating = max(best_movies.values())
    result_movies = {}

    for v in movies:
        if v in best_movies and best_movies[v] == max_rating:
            result_movies["Movie " + str(v)] = str(movies[v]) + " (+" + str(round(max_rating, 3)) + ")"

    return result_movies

if __name__ == "__main__":
    init(4)
