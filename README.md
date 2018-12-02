# resthttpck suite

## Intro
Main idea is to build a set of cli's that can be used to test part of our infrastructure supporting services we are offereing. 
Two have been built up so far: Sorenson and Vidyo. To get an understanding of what can it be achieved do:

```
python http_tester.py --help
usage: http_tester.py [-h] --c CLASSTEST --t WHICHTEST [--n NUMBEROFJOBS]

Once you are in your container running Python 3.6, in order to test Sorenson do:

Sorenson:

- Submit jobs for transcoding where you can indicate if you want to use multiple e.g. false or single e.g. true

Example: transcoding_job_true_algo  it's a single job and title is 'algo'. --n indicates how many you want to send.

    $python http_tester.py --c Sorenson --t transcoding_job_true_algo --n 1

- Query for jobs submitted in less than X hours: e.g. query_job_1 in less than one hour

$python http_tester.py --c sorenson --t query_job_1

Vidyo:

- Print the WSDL definition file in use, see config file.

Example:
    $python http_tester.py --c vidyo --t PrintWSDLdefinition

- Create a public room:

Example: where first parameter (:True) indicates if it's locked, second if it has PIN or not and,
 third if it has moderator PIN. PIN will be generated randomly.

    $python http_tester.py --c vidyo --t CreatePublicRoom:True:True:True

- Change Room profile: profile can just be 'NoAudioAndVideo' or empty one. In the latter the profile is reset. RoomID is
the first parmeter.
Example:
    $python http_tester.py --c vidyo --t ToggleRoomProfile:85589:NoAudioAndVideo

- Get Room profile
Example:
    $python http_tester.py --c vidyo --t GetRoomProfile:85593

- Update room: you indicate the extension (due to Vidyo API) and the new owner (It must already exist)
Example:
$python http_tester.py --c vidyo --t UpdateRoomOwner:109991939:XXXXXX

optional arguments:
  -h, --help        show this help message and exit
  --c CLASSTEST     Sorenson test
  --t WHICHTEST     type of job to be sent e.g. Sorenson:transcoding
  --n NUMBEROFJOBS  how many of whichtest jobs to be sent
  
  ```

## Install


