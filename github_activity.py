import sys
import urllib.request
import urllib.error
import json 

if len(sys.argv) !=3:
    print("Usage: python github_activity.py <GitHubUserName> <numberofActivitie>")
    sys.exit(1)

username=sys.argv[1]

try:
    num_act_whichWant = int(sys.argv[2])
except ValueError:
    print("Please enter a valid number for number of activities.")
    sys.exit(1)

url=f"https://api.github.com/users/{username}/events"

try:
    with urllib.request.urlopen(url) as response:
        data=json.loads(response.read().decode())
except urllib.error.HTTPError as e:
    print(f"HTTP Error: {e.code} - {e.reason}")
    sys.exit(1)
except urllib.error.URLError as e:
    print(f"Connection Error: {e.reason}")
    sys.exit(1)

if not data:
    print("!No recent activity found for this user.")
    sys.exit(0)

if len(data)>=num_act_whichWant:
    print(f"\n {username}'s last {num_act_whichWant} activities.\n")
if len(data)<num_act_whichWant:
    print(f"\n {username}: You can currently see {len(data)} activities in the system. There are less than {num_act_whichWant} records in the system. \n")
    num_act_whichWant=len(data)


for event in data[:num_act_whichWant]:
    event_type=event["type"]
    event_repo_name=event["repo"]["name"]

    if event_type == "PushEvent":
        commit_count=len(event['payload']['commits'])
        print(f"{event_type} → Pushed {commit_count} commits to {event_repo_name} repository.")

    elif event_type == "PullRequestEvent":
        print(f"{event_type} → Pull Requested sent {event_repo_name}")
    
    elif event_type == "CreateEvent":
        description = event['payload'].get('description', 'No description')
        print(f"{event_type} → Created repository.{event_repo_name}. Description:{description}")

    elif event_type == "ForkEvent":
        forked_repo = event['payload']['forkee']['full_name']
        print(f"{event_type} → Forked {forked_repo} from {event_repo_name}")

    elif event_type == "IssueCommentEvent":
        print(f"{event_type} → Issue comment sent {event_repo_name} and is {event['payload']['issue']['state']}. ")
        print(f"      Issue title: {event['payload']['issue']['title']} -> ({event['payload']['comment']['body']})")

    else:
        print(f"{event_type} → {event_repo_name}")

