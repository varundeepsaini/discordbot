from codeforces_api import CodeforcesApi
from requests import get

cf_api = CodeforcesApi()


def has_successful_submission(user_data, contest_id, problem_index):
    for submission in user_data["result"]:
        if (
            submission["verdict"] == "OK"
            and submission["problem"]["contestId"] == contest_id
            and submission["problem"]["index"] == problem_index
        ):
            return True

    return False


def get_contest_standings(contest_id):
    request_url = f"https://codeforces.com/api/contest.standings?contestId={contest_id}"
    response = get(request_url)
    response = response.json()
    return response


def getTwoProblems(username, rating):
    final_problems = [0, 0]

    url = f"https://codeforces.com/api/user.status?handle={username}"
    response = get(url)
    user_data = response.json()

    for contest in cf_api.contest_list():
        standings = get_contest_standings(contest.id)
        if standings["status"] == "OK":
            for problem in standings["result"]["problems"]:
                if final_problems[0] != 0 and final_problems[1] != 0:
                    return final_problems
                if "rating" in problem and not has_successful_submission(
                    user_data, contest.id, problem["index"]
                ):
                    if final_problems[0] != 0 and problem["rating"] == rating:
                        final_problems[0] = problem
                    if final_problems[1] != 0 and problem["rating"] == rating + 200:
                        final_problems[1] = problem

    return final_problems


print(getTwoProblems("probablyarth", 800))
