# Openshift CI Tools

Tools for working with Openshift CI

## CI Cluster Login Script

### Description
This script takes in an Openshift CI Command Cluster URL as a parameter and guides the user to `oc login` to the cluster under test.  The Command Cluster URL can be found in an early log message from the PROW build log (at the current time, this looks like: `Using namespace https://console-openshift-console.xxx.yyy.zzz/k8s/cluster/projects/ci-op-xxxx`)
. You can access PROW by clicking on the *Details* link of a `ci/prow/xxx-e2e` check on a GitHub PR.

This script is useful for getting access to a test cluster, as the ci command pod logs are ephemeral and time-sensitive.  It is recommended to run this script as soon as the above URL is available, and the script will periodically poll the necessary pods until they are ready.


### Usage
To run the script, execute: `./login_to_ci_cluster [-u COMMAND_CLUSTER_URL] [-t LOGIN_TOKEN] [-b BROWSER_COMMAND] [-h]`

Options:
- `-u COMMAND_CLUSTER_URL` - the command cluster URL, including scheme (https://) and project endpoint (/k8s/cluster/projects/ci-op-xxxxx)"
- `-t CI_CLUSTER_TOKEN` - login token to the command cluster, if known
- `-b BROWSER_COMMAND` - the shell command to pull up a browser window (given url as a param). Default: firefox
