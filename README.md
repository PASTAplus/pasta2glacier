# pasta2glacier
Archive content from the PASTA data repository to AWS Glacier

The intent of this project is to provide a mechanism to upload archived (zip or tar) data packages into Amazon's AWS Glacier storage. The archived data package would be considered a complete set of content, including the science metadata (in other words, the EML document), the quality report, and one or more data entities. Archiving (creating the zip or tar file) would take place before uploading to Glacier. A registry of completed archives would be necessary to retain a history of events and to prevent attempts to archive data packages that had previously been uploaded to Glacier.
