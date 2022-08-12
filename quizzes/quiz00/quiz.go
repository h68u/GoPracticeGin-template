package main

import "github.com/gin-gonic/gin"

func Welcome(c *gin.Context) {
	// 修改以下代码，返回 "Hello, world!"
	c.String(200, "Hello, there!")
}
