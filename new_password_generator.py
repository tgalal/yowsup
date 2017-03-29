
import json
import os

cc=raw_input('Enter Your Country Code (WITHOUT +): ')
mn=raw_input('Enter Your Mobile Number (WITHOUT COUNTRY CODE): ')
phone=cc+mn
way=raw_input('How Would You Like To Verify Your Number (VOICE/SMS): ').lower()
name=raw_input('What Is Your Good Name (FIRST NAME): ')

file=open("via-bot/CONFIG","w")
file.write("cc="+cc+"\r\n")
file.write("phone="+phone+"\r\n")
file.write("id="+"\r\n")
file.write("password="+"\r\n")
file.close()

try:
    result = os.popen("yowsup-cli registration -c via-bot/CONFIG -r "+way)
    replay=result.read()
except:
    print "\n Registration Problem"
    return 1


res_code=raw_input('Enter Responce Code Received On Your Phone [WAIT IF NOT RECEIVED]: ')

try:
    result = os.popen("yowsup-cli registration -c via-bot/CONFIG -R "+res_code)
    num_reg_details=result.read().encode('ascii','ignore')
except:
    print "Responce Code Error"
    return 1

password=num_reg_details.split()[5]

configuration={
'replayer':name,
'cc':cc,
'phone':phone,
'password':password,
}

with open('via-bot/config.json','w') as outputfile:
    json.dump(configuration,outputfile,indent=4)
