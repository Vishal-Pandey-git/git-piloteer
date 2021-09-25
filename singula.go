package main

import (
	"fmt"
	"math"
)

func main() {
	fmt.Println(pi(5000))
}

func pi(n int) float64 {
	ch := make(chan float64)
	for k := 0; k < n; k++ {
		go term(ch, float64(k))
	}
	f := 0.0
	for k := 0; k < n; k++ {
		f += <-ch
	}
	return f
}

func term(ch chan float64, k float64) {
	ch <- 4 * math.Pow(-1, k) / (2*k + 1)
}

package main

import "fmt"

const N = 11 + 1

var board = []rune(
	`...........
...........
....●●●....
....●●●....
..●●●●●●●..
..●●●○●●●..
..●●●●●●●..
....●●●....
....●●●....
...........
...........
`)
var center int

func init() {
	n := 0
	for pos, field := range board {
		if field == '○' {
			center = pos
			n++
		}
	}
	if n != 1 {
		center = -1
	}
}

var moves int
func move(pos, dir int) bool {
	moves++
	if board[pos] == '●' && board[pos+dir] == '●' && board[pos+2*dir] == '○' {
		board[pos] = '○'
		board[pos+dir] = '○'
		board[pos+2*dir] = '●'
		return true
	}
	return false
}
func unmove(pos, dir int) {
	board[pos] = '●'
	board[pos+dir] = '●'
	board[pos+2*dir] = '○'
}
func solve() bool {
	var last, n int
	for pos, field := range board {
		if field == '●' {
			for _, dir := range [...]int{-1, -N, +1, +N} {
				if move(pos, dir) {
					if solve() {
						unmove(pos, dir)
						fmt.Println(string(board))
						return true
					}
					unmove(pos, dir)
				}
			}
			last = pos
			n++
		}
	}
	if n == 1 && (center < 0 || last == center) {
		fmt.Println(string(board))
		return true
	}
	return false
}

func main() {
	if !solve() {
		fmt.Println("no solution found")
	}
	fmt.Println(moves, "moves tried")
}

