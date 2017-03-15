package main

import "encoding/json"

type ApiResponse struct {
	Ok          bool
	Description string
	Result      json.RawMessage
}

type Update struct {
	Id      int `json:"update_id"`
	Message Message
	Limit   int
}

type User struct {
	Id        int
	Username  string
	FirstName string `json:"first_name"`
	LastName  string `json:"last_name"`
}

type Chat struct {
	Id int
}

type Message struct {
	Id       int `json:"message_id"`
	From     User
	Chat     Chat
	Text     string
	Entities []MessageEntity
}

type MessageEntity struct {
	Type string
}
