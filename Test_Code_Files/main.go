package main

import (
	"fmt"
	"sort"
)

type Role int

const (
	ADMIN Role = iota
	USER
	GUEST
)

func (r Role) String() string {
	return [...]string{"ADMIN", "USER", "GUEST"}[r]
}

type User struct {
	ID   int
	Name string
	Role Role
}

type UserService struct {
	users []User
}

func NewUserService() *UserService {
	return &UserService{
		users: make([]User, 0),
	}
}

func (us *UserService) AddUser(user User) {
	us.users = append(us.users, user)
}

func (us *UserService) RemoveUserByID(id int) bool {
	for i, u := range us.users {
		if u.ID == id {
			us.users = append(us.users[:i], us.users[i+1:]...)
			return true
		}
	}
	return false
}

func (us *UserService) GetAllUsers() []User {
	return us.users
}

func (us *UserService) GetUsersByRole(role Role) []User {
	var filtered []User
	for _, u := range us.users {
		if u.Role == role {
			filtered = append(filtered, u)
		}
	}
	return filtered
}

func (us *UserService) SortUsersByName() {
	sort.Slice(us.users, func(i, j int) bool {
		return us.users[i].Name < us.users[j].Name
	})
}

func PrintUsers(title string, users []User) {
	fmt.Println(title)
	for _, u := range users {
		fmt.Printf("ID: %d, Name: %s, Role: %s\n", u.ID, u.Name, u.Role)
	}
	fmt.Println()
}

func main() {
	userService := NewUserService()

	userService.AddUser(User{ID: 1, Name: "Alice", Role: ADMIN})
	userService.AddUser(User{ID: 2, Name: "Bob", Role: USER})
	userService.AddUser(User{ID: 3, Name: "Charlie", Role: GUEST})
	userService.AddUser(User{ID: 4, Name: "Diana", Role: USER})
	userService.AddUser(User{ID: 5, Name: "Eve", Role: ADMIN})

	PrintUsers("All Users:", userService.GetAllUsers())

	userService.SortUsersByName()
	PrintUsers("Sorted Users by Name:", userService.GetAllUsers())

	PrintUsers("Admins:", userService.GetUsersByRole(ADMIN))

	fmt.Println("Removing user with ID 3...")
	removed := userService.RemoveUserByID(3)
	fmt.Printf("Removed: %v\n\n", removed)

	PrintUsers("Users After Removal:", userService.GetAllUsers())
}