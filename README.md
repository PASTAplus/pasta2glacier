# pasta2glacier
Archive content from the PASTA data repository to AWS Glacier

This project provides a mechanism to upload archived (zip or tar) data
packages from the PASTA data repository into Amazon's AWS Glacier storage. The
archived data package is considered a complete set of content, including the
science metadata (EML), the quality report, and one or more data entities.
Archiving (creating the zip or tar file) takes place before uploading to
Glacier. A registry of completed archives retains a history of events to
prevent attempts to archive data packages that had previously been uploaded to
Glacier.

Dependencies include:

- boto3
- sqlalchemy
- docopt
- awscli

Dependencies may be installed by the following command executed in the 
application root directory:

    conda env update -f environment.yml

Operation of this application requires an AWS authentication token that is 
installed into the local user's $HOME directory by the following command:

    aws configure
    
The main module for execution is "pasta2glacier". Command line usage follows:
   
    Usage: pasta2glacier.py [OPTIONS] VAULT DATA_PATH
    
      pasta2glacier provides a mechanism to upload archived (zip or tar) data
      packages from the PASTA data repository into Amazon's AWS Glacier storage.
    
      vault       The AWS Glacier vault to be used (e.g. "PASTA_Test")
      data_path   The file system path to the local data directory
    
    Options:
      -d, --dryrun     Dry run only - no AWS Glacier upload
      -n, --noclean    Do not remove tarballs after archiving
      --limit INTEGER  Limit upload to 'n' archives
      --ignore TEXT    File containing package identifiers to ignore one per line
      --workdir TEXT   Working directory path
      --lockfile TEXT  Location of lock file
      --help           Show this message and exit.
