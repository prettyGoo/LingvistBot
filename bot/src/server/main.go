package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"net/url"
	//	"reflect"
	"strconv"
	"time"
)

const (
	ApiRequest = "https://api.telegram.org/bot%s/%s"
)

var (
	httpClient http.Client
)

func main() {
	fmt.Println("LingvistBot for Telegram!\n")
	httpClient = http.Client{}
	//	getMe()

	offset := 0
	for {
		updates, _ := getUpdates(offset)
		for _, update := range updates {
			offset = update.Id + 1
		}
		fmt.Printf("%+v\n", updates)
		time.Sleep(time.Second * 1)
	}
}

// TELEGRAM API HTTP METHODS

func getMe() {
	url := fmt.Sprintf(ApiRequest, ApiToken, "getMe")
	res, _ := sendRequest(url, nil)
	fmt.Printf("%+v", res)
}

func getUpdates(offset int) ([]Update, error) {
	updates := []Update{}

	data := url.Values{}
	if offset > 0 {
		data.Add("offset", strconv.Itoa(offset))
		fmt.Println(offset)
	}

	url := fmt.Sprintf(ApiRequest, ApiToken, "getUpdates")
	r, err := sendRequest(url, data)
	if err != nil {
		return updates, err
	}

	err = json.Unmarshal(r.Result, &updates)
	if err != nil {
		return updates, err
	}

	for _, update := range updates {
		for _, entity := range updates[0].Message.Entities {
			if entity.Type == "bot_command" {
				trainCommand(update.Message.Chat.Id)
			}
		}
	}
	return updates, nil
}

func sendMessage(chat_id int, text string) {
	uri := fmt.Sprintf(ApiRequest, ApiToken, "sendMessage")

	data := url.Values{}
	data.Add("chat_id", strconv.Itoa(chat_id))
	data.Add("text", text)
	data.Add("parse_mode", "HTML")
	_, err := sendRequest(uri, data)
	if err != nil {
		fmt.Println("ERROR")
	}
}

func sendRequest(url string, data url.Values) (ApiResponse, error) {
	apiRes := ApiResponse{}

	res, err := httpClient.PostForm(url, data)
	if err != nil {
		return apiRes, err
	}

	bytes, err := ioutil.ReadAll(res.Body)
	if err != nil {
		return apiRes, err
	}

	err = json.Unmarshal(bytes, &apiRes)
	if err != nil {
		return apiRes, err
	}

	return apiRes, err
}

func trainCommand(chat_id int) {
	text := "Train is coming soon"
	sendMessage(chat_id, text)
}

func testCommand(chat_id int) {
	text := "Test is coming soon"
	sendMessage(chat_id, text)
}
