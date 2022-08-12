package main

import (
	"os"
	"time"

	"github.com/gin-gonic/gin"
)

func main() {
	r := gin.Default()
	route(r)
	go func() {
		time.Sleep(time.Second * 15)
		os.Exit(0)
	}()
	r.Run(":8081")
}

func route(e *gin.Engine) {

}
