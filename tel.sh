# request code from telegram with phone number
curl  -X POST \
  'https://tel.bot.inbeet.tech/get_code' \
  --header 'Content-Type: application/json' \
  --data-raw '{
  "phone": "989923123236"
  
}'

# login with code and password
curl  -X POST \
  'https://tel.bot.inbeet.tech/login' \
  --header 'Content-Type: application/json' \
  --data-raw '{
  "phone": "989923123236",
  "code": "73545"
}'

# send_message
curl  -X POST \
  'https://tel.bot.inbeet.tech/send_message' \
  --header 'Content-Type: application/json' \
  --data-raw '{
  "phone": "989923123236",
  "message": "salam"
}'

# logout
curl 'https://tel.bot.inbeet.tech/logout'