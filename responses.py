import random
import requests
from discord import Embed
from datetime import datetime


def fetch_upcoming_contests():
    url = "https://kontests.net/api/v1/all"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to get data from API. Status code: {response.status_code}")
        return []

    try:
        data = response.json()
    except ValueError:
        print("Failed to decode JSON data from API response.")
        return []

    print(data)  # For debugging
    upcoming_contests = []
    current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')  # Get current time in UTC
    count = 0
    for contest in data:
        if 'name' in contest and 'start_time' in contest and 'end_time' in contest:
            start_time_str = contest['start_time']
            end_time_str = contest['end_time']

            if start_time_str > current_time and count < 7:  # Check if the contest is after the current time
                try:
                    start_time = datetime.strptime(start_time_str, '%Y-%m-%dT%H:%M:%S.%fZ')
                    end_time = datetime.strptime(end_time_str, '%Y-%m-%dT%H:%M:%S.%fZ')
                except ValueError:
                    print(f"Could not parse date-time string: {start_time_str} or {end_time_str}")
                    continue

                upcoming_contests.append({
                    'Name': contest['name'],
                    'Start Time': start_time.strftime('%H:%M %d-%m-%Y'),  # Format the datetime object to a string
                    'End Time': end_time.strftime('%H:%M %d-%m-%Y'),  # Format the datetime object to a string
                    'Site': contest['site'],
                    'URL': contest['url']
                })
                count += 1

    return upcoming_contests


def codeforces_embed(formatted_response):
    handle = formatted_response['result'][0]['handle']
    name = formatted_response['result'][0]['firstName'] + " " + formatted_response['result'][0]['lastName']
    rank = formatted_response['result'][0]['rank']
    max_rank = formatted_response['result'][0]['maxRank']
    rating = formatted_response['result'][0]['rating']
    max_rating = formatted_response['result'][0]['maxRating']
    profile_url = f"https://codeforces.com/profile/{handle}"

    embed = Embed(title="Codeforces Profile", description="Here is your Codeforces Profile.", color=0x00ff00)
    embed.add_field(name="Name", value=name, inline=False)
    embed.add_field(name="Handle", value=f"[{handle}]({profile_url})", inline=False)  # hyperlink the handle
    embed.add_field(name="Rating", value=rating, inline=False)
    embed.add_field(name="Rank", value=rank.capitalize(), inline=False)
    embed.add_field(name="Max Rating", value=max_rating, inline=False)
    embed.add_field(name="Max Rank", value=max_rank.capitalize(), inline=False)

    return embed


def create_contest_embed(contests):
    embed = Embed(title="Upcoming Contests", description="Here are some upcoming coding contests.", color=0x00ff00)

    for contest in contests:
        contest_name = contest['Name']
        contest_url = contest.get('URL', 'No URL provided')
        start_time = contest['Start Time']
        end_time = contest['End Time']
        site = contest['Site']

        field_name = "Contest Details"
        field_value = f"[{contest_name}]({contest_url})\n"  # Hyperlink the contest name
        field_value += f"Start Time: {start_time}\n"
        field_value += f"End Time: {end_time}\n"
        field_value += f"Site: {site}"

        embed.add_field(name=field_name, value=field_value, inline=False)

    return embed


def codechef_embed(formatted_response, handle):
    name = formatted_response['name']
    rating = formatted_response['currentRating']
    max_rating = formatted_response['highestRating']
    stars = formatted_response['stars'][:1]
    global_rank = formatted_response['globalRank']
    country_rank = formatted_response['countryRank']
    profile_url = f"https://www.codechef.com/users/{handle}"

    embed = Embed(title="Codechef Profile", description="Here is your Codechef Profile.", color=0x00ff00)
    embed.add_field(name="Name", value=name, inline=False)
    embed.add_field(name="Handle", value=f"[{handle}]({profile_url})", inline=False)  # hyperlink the handle
    embed.add_field(name="Rating", value=rating, inline=False)
    embed.add_field(name="Max Rating", value=max_rating, inline=False)
    embed.add_field(name="Stars", value=stars, inline=False)
    embed.add_field(name="Global Rank", value=global_rank, inline=False)
    embed.add_field(name="Country Rank", value=country_rank, inline=False)

    return embed


def fetch_codechef_rating(handle):
    url = f"https://codechef-api.vercel.app/{handle}"
    response = requests.get(url)
    formatted_response = response.json()
    print(formatted_response)
    """
    Sample Response from API: 
    {'success': True, 'profile': 
    'https://cdn.codechef.com/sites/default/files/uploads/pictures/60948f5631d5838ad84e18af4e753b14.jpeg', 
    'name': 'varundeepsaini', 'currentRating': 1309, 'highestRating': 1309, 'countryFlag': 
    'https://cdn.codechef.com/download/flags/24/in.png', 'countryName': 'India', 'globalRank': 66569, 'countryRank': 
    61804, 'stars': '1★'}
    """
    if formatted_response['success']:
        return codechef_embed(formatted_response, handle)
    else:
        return "Invalid handle"


def fetch_atcoder_rating(handle):
    pass


def leetcode_embed(formatted_response, handle):
    easy_solved = formatted_response['easySolved']
    medium_solved = formatted_response['mediumSolved']
    hard_solved = formatted_response['hardSolved']
    total_solved = formatted_response['totalSolved']
    total_questions = formatted_response['totalQuestions']
    total_easy = formatted_response['totalEasy']
    total_easy_solved = formatted_response['easySolved']
    total_medium = formatted_response['totalMedium']
    total_medium_solved = formatted_response['mediumSolved']
    total_hard = formatted_response['totalHard']
    total_hard_solved = formatted_response['hardSolved']
    acceptance_rate = formatted_response['acceptanceRate']
    ranking = formatted_response['ranking']
    profile_url = f"https://leetcode.com/{handle}"

    ranking = formatted_ranking = "{:,}".format(ranking)  # Format the ranking to add commas

    embed = Embed(title="Leetcode Profile", description="Here is your Leetcode Profile.", color=0x00ff00)
    embed.add_field(name="Handle", value=f"[{handle}]({profile_url})", inline=False)  # hyperlink the handle
    embed.add_field(name="Ranking", value=ranking, inline=False)
    embed.add_field(name="Total Solved", value=f"{total_solved} / {total_questions}", inline=False)
    embed.add_field(name="Percentage Solved", value=f"{round(100 * total_solved / total_questions, 2)}%", inline=False)
    embed.add_field(name="Total Easy Solved", value=f"{total_easy_solved} / {total_easy}", inline=False)
    embed.add_field(name="Percentage Easy Solved", value=f"{round(100 * easy_solved / total_easy, 2)}%", inline=False)
    embed.add_field(name="Total Medium Solved", value=f"{total_medium_solved} / {total_medium}", inline=False)
    embed.add_field(name="Percentage Medium Solved", value=f"{round(100 * medium_solved / total_medium, 2)}%",
                    inline=False)
    embed.add_field(name="Total Hard Solved", value=f"{total_hard_solved} / {total_hard}", inline=False)
    embed.add_field(name="Percentage Hard Solved", value=f"{round(100 * hard_solved / total_hard, 2)}%", inline=False)
    embed.add_field(name="Acceptance Rate", value=f"{acceptance_rate}%", inline=False)

    return embed


def fetch_leetcode_rating(handle):
    url = f"https://leetcode-stats-api.herokuapp.com/{handle}"
    response = requests.get(url)
    formatted_response = response.json()
    print(formatted_response)

    """
    Sample Response from API: {'status': 'success', 'message': 'retrieved', 'totalSolved': 10, 'totalQuestions': 
    2863, 'easySolved': 5, 'totalEasy': 718, 'mediumSolved': 5, 'totalMedium': 1516, 'hardSolved': 0, 'totalHard': 
    629, 'acceptanceRate': 25.0, 'ranking': 2621826, 'contributionPoints': 40, 'reputation': 0, 'submissionCalendar': 
    { '1687824000': 1, '1691020800': 6, '1691107200': 17, '1692144000': 2, '1692230400': 4, '1692576000': 3, 
    '1693440000': 1, '1693872000': 1, '1693958400': 5, '1694044800': 1, '1694649600': 1, '1694995200': 1, 
    '1695081600': 1}}
    """

    if formatted_response['status'] == 'success':
        return leetcode_embed(formatted_response, handle)
    else:
        return "Invalid handle"


def fetch_hackerrank_rating(handle):
    pass


def fetch_hackerearth_rating(handle):
    pass


def fetch_codeforces_rating(handle):
    key = "55a7ead37ecd2c05638ba610904447ca89355182"
    secret = "2da790eaef6101a47d284561e1b0c743349d8121"
    url = f"https://codeforces.com/api/user.info?handles={handle}"
    response = requests.get(url)
    formatted_response = response.json()
    print(formatted_response)
    if formatted_response['status'] == 'OK':
        return codeforces_embed(formatted_response)
    else:
        return "Invalid handle"


def handleResponse(message):
    message_lower_case = message.lower()
    if message_lower_case == "hi":
        return "Hello"
    elif message_lower_case == "how are you?":
        return "I am fine, thank you"
    elif message_lower_case == 'roll':
        return str(random.randint(1, 6))
    elif message_lower_case == 'flip':
        return random.choice(['Heads', 'Tails'])
    elif message_lower_case == 'contests':
        contests = fetch_upcoming_contests()
        return create_contest_embed(contests)  # Return the embed object
    elif message_lower_case[:7] == 'profile':
        message_split = message[7:].split()
        if len(message_split) == 2:
            platform = message_split[0].lower()
            handle = message_split[1]
            if platform == 'codeforces':
                rating = fetch_codeforces_rating(handle)
                return rating
            elif platform == 'codechef':
                rating = fetch_codechef_rating(handle)
                return rating
            elif platform == 'leetcode':
                rating = fetch_leetcode_rating(handle)
                return rating
            elif platform == 'atcoder':
                rating = fetch_atcoder_rating(handle)
                return rating
            elif platform == 'hackerrank':
                rating = fetch_hackerrank_rating(handle)
                return rating
            elif platform == 'hackerearth':
                rating = fetch_hackerearth_rating(handle)
                return rating

        return "Invalid command. Please use the format `rating <platform> <handle>`"

    elif message_lower_case == 'help':
        return "DM varun and ask, he was too lazy to add documentation here, btw **vis op**"
