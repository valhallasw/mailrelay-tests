# mailrelay-tests
Tests for tool labs mailrelay servers

Requirements:
  - Eximunit [1] with extra routing test functionality [2]
  - A mailrelay host

Files:
  - `offline_tests.py` tests 
    - responses to SMTP (mail acceptance)
    - routing (address rewriting / accepted users)

Files (to write):
  - `online_tests.py` tests
    - actual delivery to gmail
    - actual SMTP from outside (not sure yet how to test)
  - `dns_tests.py` tests
    - spf
    - forward and reverse dns
    - check if matches with exim config

[1] https://bitbucket.org/davidnorth/eximunit
[2] https://bitbucket.org/valhallasw/eximunit/branch/stderr_log
