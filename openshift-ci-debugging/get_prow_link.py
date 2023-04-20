#!/usr/bin/env python
import argparse
import requests
from bs4 import BeautifulSoup
import re

# Selenium Requirements
import time 
from selenium import webdriver 


PROW_FMT = "https://prow.ci.openshift.org/log?container={}&id={}&job={}"
CLUSTER_REGEX = r'Using namespace \S+'


# TODO: handle logging into GitHub to see the checks
def get_e2e_from_pr(pr_link):
    sel_driver = _init_selenium()
    data = get_github_html_data(pr_link, sel_driver)
    assert data
    checks = get_check_links(data)
    assert checks
    e2e_link = get_e2e_check(checks)
    assert e2e_link
    return get_ci_cluster(e2e_link)

# TODO: need to log into GitHub to see checks, currently just
# hope they've logged in by the 20s timer which is awful 
def get_github_html_data(url, driver):
    driver.get(url)
    time.sleep(20)
    htmldata = driver.page_source
    driver.close()
    print(htmldata)
    return htmldata


def get_ci_cluster(e2e_link):
    e2e_id, e2e_job, e2e_container = get_e2e_log(e2e_link)
    assert e2e_id
    prow_link = get_prow_link(e2e_id, e2e_job, e2e_container)
    assert prow_link
    cluster_url = parse_url_from_log(prow_link)
    assert cluster_url
    return cluster_url


def get_check_links(html_data):
    soup = BeautifulSoup(html_data, 'html.parser')
    return soup.find_all("a", {"class": "status-actions"})


def get_e2e_check(check_list):
    for l in check_list:
        href = l['href']
        if 'e2e' in href:
            return href
    
def get_e2e_log(e2e_link):
    splits = e2e_link.split("/")
    id = splits[-1]
    job = splits[-2]
    container = 'test'  # TODO: is it always 'test'?  Need deterministic way to get this.
    return id, job, container


def get_prow_link(id, job, container="test"):
    return PROW_FMT.format(container, id, job)


def parse_url_from_log(prow_link):
    logdata = _get_html_page(prow_link)
    matches = re.findall(CLUSTER_REGEX, logdata)
    if len(matches) > 0:
        return matches[0].split()[2]
    return None

def _init_selenium():
    return webdriver.Firefox()

def _get_html_page(url):
    return requests.get(url).text


def parse_args():
    args = argparse.ArgumentParser()
    args.add_argument("-u", "--url", required=True)
    return args.parse_args()


def main():
    args = parse_args()
    print(get_ci_cluster(args.url))


if __name__ == '__main__':
    main()

