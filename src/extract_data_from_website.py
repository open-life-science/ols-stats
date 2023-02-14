#!/usr/bin/env python

import argparse
import base64
import copy
import datetime
import pandas as pd
import yaml

from github import Github
from pathlib import Path

actual_cohort = 7

def read_yaml_file(fp, ref):
    '''
    Read a YAML file at a given git commit

    :param fp: path to file on GitHub
    :param ref: name of the commit/branch/tag

    :return: set with contributor ids
    '''
    file_content = repo.get_contents(fp, ref=ref).content
    decoded_file_content = base64.b64decode(file_content)
    return yaml.load(decoded_file_content, Loader=yaml.FullLoader)


def update_people_info(p_list, p_dict, status, cohort_id):
    '''
    Update people attribute for a cohort

    :param p_list: list of people id to update
    :param p_dict: dictionary with people information
    :param status: status to add
    :param cohort_id: concerned cohort
    '''
    for p in p_list:
        if p is None:
            continue
        if p not in p_dict:
            print(f"{p} not found in people")
            continue
        p_dict[p][f'ols-{cohort_id}'].append(status)


def get_people_names(p_list, p_dict):
    '''
    Get names of peoke
    
    :param p_list: list of people id
    :param p_dict: dictionary with people information
    '''
    names = []
    for p in p_list:
        if p is None:
            names.append(None)
        elif p not in p_dict:
            print(f"{p} not found in people")
            names.append(None)
        else:
            names.append(f"{p_dict[p]['first-name']} {p_dict[p]['last-name']}")
    return names


def get_people():
    '''
    Get people information
    '''
    people = read_yaml_file("_data/people.yaml", "main")
    # remove some keys and add space for cohorts
    for key, value in people.items():
        value.pop('affiliation', None)
        value.pop('bio', None)
        value.pop('orcid', None)
        value.pop('twitter', None)
        value.pop('website', None)
        value.pop('github', None)
        value.pop('title', None)
        value.pop('expertise', None)
        for i in range(1, actual_cohort+1):
            value[f'ols-{i}'] = []
    return people


def extract_cohort_information(people):
    '''
    Get cohort and project informations
    '''
    projects = []
    for i in range(1, actual_cohort+1):
        print(f"OLS {i}")
        # extract experts, facilitators, organizers from metadata
        metadata = read_yaml_file(f"_data/ols-{i}-metadata.yaml" , "main")
        update_people_info(metadata['experts'], people, 'expert', i)
        if 'facilitators' in metadata:
            update_people_info(metadata['facilitators'], people, 'facilitator', i)
        update_people_info(metadata['organizers'], people, 'organizer', i)
        # extract participants, mentors from projects
        # extract project details
        cohort_projects = read_yaml_file(f"_data/ols-{i}-projects.yaml", "main")
        for p in cohort_projects:
            # update participant and mentor information
            update_people_info(p['participants'], people, 'participant', i)
            update_people_info(p['mentors'], people, 'mentor', i)
            # get project details
            pr = copy.copy(p)
            pr['participants'] = get_people_names(p['participants'], people)
            pr['mentors'] = get_people_names(p['mentors'], people)
            pr['cohort'] = i
            pr['keywords'] = p['keywords'] if 'keywords' in p else []
            projects.append(pr)
        # extract speakers from schedule
        schedule = read_yaml_file(f"_data/ols-{i}-schedule.yaml", "main")
        for w, week in schedule['weeks'].items():
            for c in week['calls']:
                if c['type'] == 'Cohort' and 'resources' in c and c['resources'] is not None:
                    for r in c['resources']:
                        if r['type'] == 'slides' and 'speaker' in r and r['speaker'] is not None:
                            update_people_info([r['speaker']], people, 'speaker', i)
    return projects, people


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract data from website into CSV files')
    parser.add_argument('-t', '--token', help="GitHub token", required=True)
    parser.add_argument('-o', '--out', help="Path to output folder", required=True)
    args = parser.parse_args()

    # connect to GitHub
    g = Github(args.token)
    # to get limit of API request: g.get_rate_limit()
    # retrieve the hub repository
    repo = g.get_user("open-life-science").get_repo("open-life-science.github.io")

    # get people information
    people = get_people()

    # get cohort and project informations
    projects, people = extract_cohort_information(people)

    # export people information to CSV file
    people_df = pd.DataFrame.from_dict(people, orient='index')
    for i in range(1, actual_cohort+1):
        people_df[f'ols-{i}'] = people_df[f'ols-{i}'].apply(lambda x: ', '.join([str(i) for i in x]))
    people_fp = Path(args.out) / Path('people.csv')
    people_df.to_csv(people_fp)

    # export project information to CSV file
    project_df = pd.DataFrame(projects)
    project_df['participants'] = project_df['participants'].apply(lambda x: ', '.join([str(i) for i in x]))
    project_df['mentors'] = project_df['mentors'].apply(lambda x: ', '.join([str(i) for i in x]))
    project_df['keywords'] = project_df['keywords'].apply(lambda x: ', '.join([str(i) for i in x]))
    project_fp = Path(args.out) / Path('projects.csv')
    project_df.to_csv(project_fp)









    