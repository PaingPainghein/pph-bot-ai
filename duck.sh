#!/bin/bash
DOMAIN="pphaibot"  # Duck DNS subdomain (".duckdns.org" မထည့်ပါ)
TOKEN="b35bcc09-d172-4dce-9d38-43942692dc2e"  # သင့် token
echo url="https://www.duckdns.org/update?domains=$DOMAIN&token=$TOKEN&ip=" | curl -o ~/duckdns/duck.log -K -
