# email-and-sms-api
## Redis_lua_nginx
A utility to push data to redis using Lua on ngynx

First we make our nginx executable of our OpenResty installation available in our PATH environment:
```
PATH=/usr/local/openresty/nginx/sbin:$PATH
export PATH
```
Then we start the nginx server with our config file this way:
```
nginx -p `pwd`/ -c conf/nginx.conf
```

Using Curl, data can be pushed to REDIS in Json

Example :

```
 curl -v -XPOST -d '{"message" : "lets go shopping" , "message_type": "info", "mobile_no": "9199999999999"}' http://localhost:8080/sms

```

##celery
```
celery -A tasks worker --loglevel=info --beat
```
display the data on mongnoDB data base

using commandline on new shell
>show dbs
#my_sms_db
>use my_sms_dbs
##switched to db my_sms_db
>show collections
#sms
>db.sms.find().pretty()
    
    {
	"_id" : ObjectId("559cc9f54170de223566e652"),
	"message" : "lets go shopping ",
	"message_type" : "info",
	"mobile" : [
		"919999999999"
	]
}



