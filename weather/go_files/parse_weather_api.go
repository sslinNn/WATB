package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"strings"
)

type HourlyData struct {
	Time      string  `json:"time"`
	TempC     float64 `json:"temp_c"`
	Condition struct {
		Text string `json:"text"`
	} `json:"condition"`
	WindKph float64 `json:"wind_kph"`
}

func main() {
	data, err := ioutil.ReadFile("input.json")
	if err != nil {
		fmt.Println("Ошибка чтения файла:", err)
		return
	}

	var perHour []HourlyData
	err = json.Unmarshal(data, &perHour)
	if err != nil {
		fmt.Println("Ошибка разбора JSON:", err)
		return
	}

	hour := []string{}
	tempC := []float64{}
	condition := []string{}
	wind := []float64{}

	for _, i := range perHour {
		hourParts := strings.Split(i.Time, " ")
		hour = append(hour, hourParts[1])
		tempC = append(tempC, i.TempC)
		condition = append(condition, i.Condition.Text)
		wind = append(wind, i.WindKph)
	}

	outputData := struct {
		Hour      []string
		TempC     []float64
		Condition []string
		WindKph   []float64
	}{
		Hour:      hour,
		TempC:     tempC,
		Condition: condition,
		WindKph:   wind,
	}

	outputJSON, err := json.Marshal(outputData)
	if err != nil {
		fmt.Println("Ошибка при создании JSON:", err)
		return
	}

	err = ioutil.WriteFile("output.json", outputJSON, 0644)
	if err != nil {
		fmt.Println("Ошибка записи в файл:", err)
		return
	}

	fmt.Println("Данные сохранены в output.json")
}
