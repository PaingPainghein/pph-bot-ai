#!/bin/bash
echo url="https://www.duckdns.org/update?domains=pphaibot&token=b35bcc09-d172-4dce-9d38-43942692dc2e&ip=" | curl -k -o ~/duckdns/duck.log -K -
