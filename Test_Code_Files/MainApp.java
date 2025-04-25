import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;

enum Role {
    ADMIN, USER, GUEST
}

class User {
    private int id;
    private String name;
    private Role role;

    public User(int id, String name, Role role) {
        this.id = id;
        this.name = name;
        this.role = role;
    }

    public int getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public Role getRole() {
        return role;
    }

    public String toString() {
        return "User{id=" + id + ", name='" + name + "', role=" + role + "}";
    }
}

class UserService {
    private List<User> users;

    public UserService() {
        users = new ArrayList<>();
    }

    public void addUser(User user) {
        users.add(user);
    }

    public boolean removeUserById(int id) {
        return users.removeIf(u -> u.getId() == id);
    }

    public List<User> getAllUsers() {
        return users;
    }

    public List<User> getUsersByRole(Role role) {
        List<User> filtered = new ArrayList<>();
        for (User user : users) {
            if (user.getRole() == role) {
                filtered.add(user);
            }
        }
        return filtered;
    }

    public void sortUsersByName() {
        Collections.sort(users, Comparator.comparing(User::getName));
    }
}

public class MainApp {
    public static void main(String[] args) {
        UserService userService = new UserService();

        userService.addUser(new User(1, "Alice", Role.ADMIN));
        userService.addUser(new User(2, "Bob", Role.USER));
        userService.addUser(new User(3, "Charlie", Role.GUEST));
        userService.addUser(new User(4, "Diana", Role.USER));
        userService.addUser(new User(5, "Eve", Role.ADMIN));

        System.out.println("All Users:");
        for (User user : userService.getAllUsers()) {
            System.out.println(user);
        }

        System.out.println("\nSorted Users by Name:");
        userService.sortUsersByName();
        for (User user : userService.getAllUsers()) {
            System.out.println(user);
        }

        System.out.println("\nAdmins:");
        for (User user : userService.getUsersByRole(Role.ADMIN)) {
            System.out.println(user);
        }

        System.out.println("\nRemoving user with ID 3");
        boolean removed = userService.removeUserById(3);
        System.out.println("Removed: " + removed);

        System.out.println("\nUsers After Removal:");
        for (User user : userService.getAllUsers()) {
            System.out.println(user);
        }
    }
}