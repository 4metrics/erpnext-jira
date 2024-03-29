# Copyright (c) 2021, ALYF GmbH and contributors
# Copyright (c) 2024, 4metrics Software GmbH and contributors

from typing import Iterator

import requests
from requests.auth import HTTPBasicAuth

import frappe

from .jira_issue import JiraIssue
from .jira_worklog import JiraWorklog


class JiraClient:
	def __init__(self, url, user, api_key) -> None:
		self.url = url
		self.session = requests.Session()
		self.session.auth = HTTPBasicAuth(user, api_key)
		self.session.headers = {"Accept": "application/json"}

	def get(self, url: str, params=None):
		response = self.session.get(url, params=params)

		try:
			response.raise_for_status()
		except requests.HTTPError:
			frappe.log_error(frappe.get_traceback())
			return {}

		return response.json()

	def get_issues(self, project: str) -> "Iterator[JiraIssue]":
		url = f"{self.url}/rest/api/3/search"
		params = {
			"jql": f"project = {project} AND worklogDate > 0 ORDER BY created ASC",
			"fields": "summary",
			"startAt": 0,
			"maxResults": 100,
		}

		while True:
			response = self.get(url, params=params)

			if not response:
				break

			params["startAt"] += response["maxResults"]

			for issue in response.get("issues"):
				yield JiraIssue.from_dict(issue)

			if response.get("total") <= params["startAt"]:
				break

	def get_worklogs(self, issue: str) -> "list[JiraWorklog]":
		url = f"{self.url}/rest/api/3/issue/{issue}/worklog"
		params = {
			"startAt": 0,
			"maxResults": 100
		}

		while True:
			response = self.get(url, params=params)

			if not response:
				break

			params["startAt"] += response["maxResults"]

			for worklog in response.get("worklogs"):
				yield JiraWorklog.from_dict(worklog)

			if response.get("total") <= params["startAt"]:
				break
