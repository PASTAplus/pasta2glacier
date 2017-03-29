# pasta2glacier
Archive content from the PASTA data repository to AWS Glacier

This project provides a mechanism to upload archived (zip or tar) data
packages into Amazon's AWS Glacier storage. The archived data package is
considered a complete set of content, including the science metadata (EML),
the quality report, and one or more data entities. Archiving (creating the zip
or tar file) takes place before uploading to Glacier. A registry of completed
archives retains a history of events to prevent attempts to archive data
packages that had previously been uploaded to Glacier.

![image of sequence diagram](https://www.planttext.com/plantuml/img/PP2n2W8n38RtF4Lnqk4GRxn1L8Hp57INj1SqMDkIje9lRyNpv7GA2V_taMGL4qhADmkGE5bIa_twS5nNTTLQD4mo0T0-kmxbeNPPX0qwWb0WDXpG9HMmEEhpEmuT9jGOIVM3xURBzqg04L8j1s-ZBCTqwbZ892zCSJhNQAuvp5_UnGoiz-4N7xMDqfbjfr3CXU_qcsq_gKZk6-gdrPzBA0RlufzcEAvixC-3fpW1O5LA-UWJ)