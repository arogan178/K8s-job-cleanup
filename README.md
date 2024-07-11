# Kubernetes Job Cleanup Script

This Python script is designed to clean up Kubernetes jobs that have either completed or failed and are older than one day. It also deletes any dependent pods associated with those jobs.

## Prerequisites

- Python 3.6+
- `kubectl` configured to access your Kubernetes cluster
- Necessary permissions to list and delete jobs and pods in the target namespace
- If using OpenShift, ensure you are logged in with `oc login`

## Installation

1. **Clone the repository**:

    ```sh
    git clone https://github.com/arogan178/K8s-job-cleanup.git
    cd K8s-job-cleanup
    ```

2. **Set up a virtual environment (optional but recommended)**:

    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install required packages**:

    No external packages are required for this script.

## Usage

1. **Run the script**:

    ```sh
    python cleanup_jobs.py
    ```

2. **Enter the namespace**:

    When prompted, enter the namespace where the jobs are located.

## How It Works

- The script lists all jobs in the specified namespace.
- For each job, it checks the last run time.
- It calculates the time difference between the current time and the job's last run time.
- If the job is completed or failed and older than one day, it deletes the job and its dependent pods.

## Contributing

If you find a bug or have a suggestion for improvement, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
