import requests


def getTwoProblems(username, rating):
    rounded_rating = round(rating / 100) * 100
    higher_rating = rounded_rating + 200

    submissions_url = (
        f"https://codeforces.com/api/user.status?handle={username}&from=1&count=1000000"
    )
    response = requests.get(submissions_url)
    data = response.json()
    if data["status"] != "OK":
        return []

    solved_problems = set()
    for submission in data["result"]:
        if submission["verdict"] == "OK":
            problem_id = (
                submission["problem"]["contestId"],
                submission["problem"]["index"],
            )
            solved_problems.add(problem_id)

    problems_url = "https://codeforces.com/api/problemset.problems"
    response = requests.get(problems_url)
    data = response.json()
    if data["status"] != "OK":
        return []

    selected_problems = []
    for problem in data["result"]["problems"]:
        if "rating" not in problem:
            continue
        if (
            problem["rating"] == rounded_rating
            and (problem["contestId"], problem["index"]) not in solved_problems
        ):
            selected_problems.append(problem)
            if len(selected_problems) == 2:
                break
        elif (
            problem["rating"] == higher_rating
            and (problem["contestId"], problem["index"]) not in solved_problems
        ):
            selected_problems.append(problem)
            if len(selected_problems) == 2:
                break

    return selected_problems
