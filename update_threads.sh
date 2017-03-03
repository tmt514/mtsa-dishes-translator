
##################################################################
##################################################################
###
###  YOU MUST DELETE PAGE_TOKEN AFTER YOU RUN THE SCRIPT
###
###  DO NOT COMMIT PAGE_TOKEN !!!
###
##################################################################
##################################################################
PAGE_TOKEN=


curl -X POST -H "Content-Type: application/json" -d '{ 
  "get_started":{
    "payload":"GET_STARTED_PAYLOAD"
  }
}' "https://graph.facebook.com/v2.8/me/messenger_profile?access_token=$PAGE_TOKEN"

curl -X POST -H "Content-Type: application/json" -d '{
  "persistent_menu":[
				{
						"locale": "default",
						"composer_input_disabled": false,
						"call_to_actions": [
								{
										"type":"postback",
										"title":"答題大挑戰",
										"payload":"STATE_QA_CHALLENGE"
								},
								{
										"type":"postback",
										"title":"查詢寶可夢",
										"payload":"PAYLOAD_POKEMON_SEARCH"
								},
								{
										"type":"nested",
										"title":"安城美食探索小遊戲",
										"call_to_actions": [
												{
														"type": "postback",
														"title": "查看玩家資料",
														"payload": "PAYLOAD_GAME_DATA"
												},
												{
														"type": "postback",
														"title": "新的探索任務",
														"payload": "PAYLOAD_GAME_MISSION"
												},
												{
														"type": "postback",
														"title": "查看任務列表",
														"payload": "PAYLOAD_GAME_LIST_MISSION"
												},
												{
                          "type": "postback",
                          "title": "查看道具列表",
                          "payload": "PAYLOAD_GAME_ITEM"
                      }
                  ]
              }
         ]
    }
  ]
}' "https://graph.facebook.com/v2.8/me/messenger_profile?access_token=$PAGE_TOKEN"
   
