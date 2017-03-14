package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
)

const (
	ApiToken   = "373643335:AAGQ_V1j7yV1kWMHdR-3RSc0tW44tioeY2Y"
	ApiRequest = "https://api.telegram.org/bot%s/%s"
)

var (
	httpClient http.Client
)

func main() {
	fmt.Println("LingvistBot for Telegram!\n")
	httpClient = http.Client{}
	//	getMe()
	updates, _ := getUpdates()
	fmt.Printf("%+v\n", updates)

	chat_id := updates[0].Message.Chat.Id
	sendMessage(chat_id)

}

// TELEGRAM API HTTP METHODS

func getMe() {
	url := "https://api.telegram.org/bot373643335:AAGQ_V1j7yV1kWMHdR-3RSc0tW44tioeY2Y/getMe"
	res := sendRequest(url, nil)
	fmt.Printf("%+v", res)
}

func getUpdates() ([]Update, error) {
	const methodName = "getUpdates"
	updates := []Update{}

	r := sendRequest("https://api.telegram.org/bot373643335:AAGQ_V1j7yV1kWMHdR-3RSc0tW44tioeY2Y/getUpdates", nil)
	//	if err != nil {
	//		return updates, err
	//	}

	err := json.Unmarshal(r.Result, &updates)
	if err != nil {
		return updates, err
	}

	return updates, nil
}

func sendMessage(chat_id int) {
	url := "https://api.telegram.org/bot373643335:AAGQ_V1j7yV1kWMHdR-3RSc0tW44tioeY2Y/sendMessage"
	data := url.Values{}
	 data.Add("chat_id", strconv.Itoa(msg.ChatId))
	 data.Add("text", msg.Text)
	 data.Add("parse_mode", msg.ParseMode)
	sendRequest(url, data)
}

func sendRequest(url string, data url Values) ApiResponse {
	apiRes := ApiResponse{}

	res, err := httpClient.PostForm(url, data)
	if err != nil {
		panic(err)
	}

	bytes, err := ioutil.ReadAll(res.Body)

	_ = json.Unmarshal(bytes, &apiRes)
	return apiRes
}
