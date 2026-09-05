#Name: Brennan Adams
#Class: INF601 Advanced Programming with Python
#Mini Project 1

import os
import requests

BASE = "https://practice.fhsucyber.com"
TOKEN = os.environ.get("PRACTICE_API_TOKEN")


class PracticeHubClient:
    def __init__(self, base_url, token):
        self.base = base_url.rstrip("/")
        self.headers = {"Authorization": f"Bearer {token}"}

    def create_post(self, title, body="", tags=None):
        if(not self.status_check()):
            return
        resp = requests.post(f"{self.base}/api/v1/posts", headers=self.headers,
                             json={"title": title, "body": body, "tags": tags or []})
        return resp.json()

    def list_posts(self, mine=False, tag=None):
        params = {"mine": mine}
        if tag:
            params["tag"] = tag

        resp = requests.get(f"{self.base}/api/v1/posts", headers=self.headers, params=params)
        return resp.json()

    def get_post(self, post_id: int):
        if(not self.status_check(post_id)):
           return
        resp = requests.get(f"{self.base}/api/v1/posts/{post_id}", headers=self.headers)
        resp.raise_for_status()
        return resp.json()

    def update_post(self, post_id: int, body: str):
        if(not self.status_check(post_id)):
            return
        post = requests.patch(f"{self.base}/api/v1/posts/{post_id}", headers=self.headers, json={"body": body})
        post.raise_for_status()
        return post.json()

    def delete_post(self, post_id: int) -> bool:
        if(not self.status_check(post_id)):
            return False
        requests.delete(f"{self.base}/api/v1/posts/{post_id}", headers=self.headers)
        return True

    def status_check(self, post_id: int=0) -> bool:
        resp=requests.get(f"{self.base}/api/v1/posts/{post_id}", headers=self.headers)
        if(resp.status_code==401):
            print("401 Error: Token is missing or invalid. Please resubmit the token into environment variables.")
            return False
        if(post_id==0):
            return True
        elif(resp.status_code==404):
            print("404 Error: Post does not exist.")
            return False
        elif(resp.status_code==403):
            print("403 Error: Attempting to edit someone else's post.")
            return False
        elif(resp.status_code==422):
            print("422 Error: Field is either missing or is too short. Please ensure that all parameters are valid.")
            return False
        return True

if __name__ == "__main__":
    if not TOKEN:
        raise SystemExit("PRACTICE_API_TOKEN is not set - see 'Set your token' in Week 2.")

    client = PracticeHubClient(BASE, TOKEN)

    #everyone = client.list_posts()
    #print(f"posts on the hub: {len(everyone)}")

    #new_post = client.create_post("Week 3 lab", body="My first created post.")
    #print(f"created post {new_post['id']}: {new_post['title']}")

    #print(f"posts that are mine: {len(client.list_posts(mine=True))}")

    post_id = 9

    print(f"Created Post: {client.create_post(post_id,"test")}")
    print(f"Updated Post: {client.update_post(post_id,"edit")}")
    client.delete_post(post_id)
    client.delete_post(post_id)
