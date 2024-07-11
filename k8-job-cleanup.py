#!/usr/bin/env python3

import subprocess
import json
from datetime import datetime, timezone, timedelta

def get_namespace():
    return input("Enter the namespace where the jobs are located: ")

def run_kubectl_command(command):
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise Exception(f"Error running command: {command}\n{result.stderr}")
    return result.stdout

def get_jobs(namespace):
    command = f"kubectl get jobs -n {namespace} -o json"
    output = run_kubectl_command(command)
    jobs = json.loads(output)['items']
    return jobs

def get_last_run_time(job):
    last_run_time_str = job['status'].get('completionTime') or job['status'].get('startTime')
    if not last_run_time_str:
        return None
    last_run_time = datetime.fromisoformat(last_run_time_str.replace("Z", "+00:00"))
    return last_run_time

def delete_job(job_name, namespace):
    command = f"kubectl delete job {job_name} -n {namespace}"
    run_kubectl_command(command)

def delete_dependent_pods(job_name, namespace):
    command = f"kubectl delete pods --field-selector=status.phase==Failed -l job-name={job_name} -n {namespace}"
    run_kubectl_command(command)

def main():
    namespace = get_namespace()
    jobs = get_jobs(namespace)
    now = datetime.now(timezone.utc)
    one_day_ago = now - timedelta(days=1)

    for job in jobs:
        job_name = job['metadata']['name']
        last_run_time = get_last_run_time(job)
        if last_run_time is None:
            print(f"Job {job_name} has no last run time, skipping...")
            continue

        time_diff = (now - last_run_time).total_seconds()

        completed = job['status'].get('succeeded', 0) > 0
        failed = job['status'].get('failed', 0) > 0

        print(f"Checking job {job_name}...")
        print(f"  Last run time: {last_run_time}")
        print(f"  Time difference (seconds): {time_diff}")
        print(f"  Completed status: {completed}")
        print(f"  Failed status: {failed}")

        if (completed or failed) and time_diff > 86400:
            print(f"  Deleting job {job_name} and its dependent pods...")
            delete_job(job_name, namespace)
            delete_dependent_pods(job_name, namespace)
            print(f"Deleted job {job_name} and its dependent pods")

if __name__ == "__main__":
    main()
