package main

import "github.com/gin-gonic/gin"

func main() {
	r := gin.Default()
	r.GET("/", func(ctx *gin.Context) {
		// 按要求修改，被访问时应返回 Hello, world!
		ctx.String(200, `Replace here with "Hello, world!"`)
	})

	r.Run(":8081")
}
