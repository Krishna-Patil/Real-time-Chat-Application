import pandas as pd


def extract_token_ws(headers):
    """
    extracts jwt token from websocket connection headers
    """
    try:
        for key, value in headers:
            if key == b"authorization":
                token = value.decode("utf8").split()[1]
                return token
    except Exception as e:
        return e


def suggest_friends(user_id):
    """
    recommends friends based on interests
    """
    recommended = []
    queries = []
    # Reading the input from file
    json_data = pd.read_json("users.json")
    users_datagram = pd.json_normalize(json_data["users"])
    # getting user's interests
    user_interests = (
        users_datagram.loc[user_id - 1]
        .drop(["name", "age", "id"])
        .dropna()
        .sort_values(ascending=False)
    )
    user_interests_dict = user_interests.to_dict()
    df1 = users_datagram.loc[:, [col for col in user_interests.index]]
    # settings conditions to recommend
    # where interests are similar or greater than the user's interests
    # that we are looking for
    conditions = [
        f"`{str(col)}` >= {user_interests_dict[str(col)]}" for col in df1.columns
    ]
    query = " & ".join(conditions)
    for i in range(len(df1.columns), 0, -1):
        queries.append(" & ".join(conditions[:i]))
    # getting recommended id's
    for query in queries:
        recommended.extend(list(users_datagram.query(query)["id"]))
    # removing duplicates while preserving order
    recommended = dict.fromkeys(recommended)
    recommended.pop(user_id)
    # filtering data for only recommended users
    recommended_datagram = users_datagram[users_datagram["id"].isin(recommended)]
    # sorting data according to our priorities
    recommended_datagram["sort"] = pd.Categorical(
        recommended_datagram["id"], categories=recommended, ordered=True
    )
    top_five_recommendations = recommended_datagram.sort_values("sort").head()
    top_five_recommendations.drop(["sort"], axis=1, inplace=True)
    # removing null values
    res = [dict(row.dropna()) for idx, row in top_five_recommendations.iterrows()]
    return res
