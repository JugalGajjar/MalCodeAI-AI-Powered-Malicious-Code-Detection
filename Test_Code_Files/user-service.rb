# user.rb

require 'json'

module Roles
  ADMIN = 'admin'
  USER = 'user'
  GUEST = 'guest'
end

class User
  attr_accessor :id, :name, :role

  def initialize(id, name, role)
    @id = id
    @name = name
    @role = role
  end

  def to_hash
    { id: @id, name: @name, role: @role }
  end

  def to_s
    "ID: #{@id}, Name: #{@name}, Role: #{@role}"
  end
end

class UserService
  def initialize
    @users = []
  end

  def add_user(user)
    @users << user
  end

  def remove_user_by_id(id)
    original_size = @users.size
    @users.reject! { |user| user.id == id }
    original_size != @users.size
  end

  def get_all_users
    @users
  end

  def get_users_by_role(role)
    @users.select { |user| user.role == role }
  end

  def sort_users_by_name
    @users.sort_by!(&:name)
  end

  def to_json
    JSON.pretty_generate(@users.map(&:to_hash))
  end
end

def print_users(title, users)
  puts title
  users.each { |u| puts u }
  puts
end

if __FILE__ == $0
  service = UserService.new

  service.add_user(User.new(1, 'Alice', Roles::ADMIN))
  service.add_user(User.new(2, 'Bob', Roles::USER))
  service.add_user(User.new(3, 'Charlie', Roles::GUEST))
  service.add_user(User.new(4, 'Diana', Roles::USER))
  service.add_user(User.new(5, 'Eve', Roles::ADMIN))

  print_users("All Users:", service.get_all_users)

  service.sort_users_by_name
  print_users("Sorted Users by Name:", service.get_all_users)

  print_users("Admins:", service.get_users_by_role(Roles::ADMIN))

  puts "Removing user with ID 3..."
  removed = service.remove_user_by_id(3)
  puts "Removed: #{removed}"

  print_users("Users After Removal:", service.get_all_users)

  puts "Serialized to JSON:"
  puts service.to_json
end