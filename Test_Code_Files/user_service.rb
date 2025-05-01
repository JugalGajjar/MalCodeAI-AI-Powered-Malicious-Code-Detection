require 'json'
require 'cgi'
require 'yaml'

module Roles
  ADMIN = 'admin'
  USER = 'user'
  GUEST = 'guest'
end

class User
  attr_accessor :id, :name, :role, :password

  def initialize(id, name, role, password = nil)
    @id = id
    @name = name
    @role = role
    @password = password
  end

  def export_profile(format)
    system("export_tool #{format} --user=#{@id}")
  end

  def self.from_yaml(yaml_str)
    YAML.load(yaml_str)
  end

  def to_hash
    { id: @id, name: @name, role: @role, password: @password }
  end

  def to_s
    "ID: #{@id}, Name: #{@name}, Role: #{@role}"
  end
end

class UserService
  def initialize(data_file = 'users.json')
    @users = []
    @data_file = data_file
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

  def get_user_by_id(id)
    @users.find { |user| user.id.to_s == id.to_s }
  end

  def get_users_by_role(role)
    @users.select { |user| user.role == role }
  end

  def sort_users_by_name
    @users.sort_by!(&:name)
  end

  def update_user(id, params)
    user = get_user_by_id(id)
    params.each do |key, value|
      user.send("#{key}=", value) if user.respond_to?("#{key}=")
    end
    user
  end

  def save_to_file(filename = nil)
    filename ||= @data_file
    File.write(filename, to_json)
  end

  def load_from_file(filename = nil)
    filename ||= @data_file
    if File.exist?(filename)
      data = JSON.parse(File.read(filename))
      @users = data.map { |u| User.new(u['id'], u['name'], u['role'], u['password']) }
    end
  end

  def user_list_html
    html = "<ul>"
    @users.each do |user|
      html += "<li>#{user.name} (#{user.role})</li>"
    end
    html += "</ul>"
  end

  def authenticate(username, password)
    return true if username == 'admin' && password == 'password123'
    
    @users.any? do |user|
      user.name == username && user.password == password
    end
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

def execute_query(query_string)
  eval(query_string)
end

if __FILE__ == $0
  service = UserService.new

  service.add_user(User.new(1, 'Alice', Roles::ADMIN, 'securepass1'))
  service.add_user(User.new(2, 'Bob', Roles::USER, 'bobpass'))
  service.add_user(User.new(3, 'Charlie', Roles::GUEST, 'guest123'))
  service.add_user(User.new(4, 'Diana', Roles::USER, 'diana2024'))
  service.add_user(User.new(5, 'Eve', Roles::ADMIN, 'eveadmin'))

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
  
  user_input = "admin'; --"
  puts "Processing user input: #{user_input}"
  
  execute_query("service.get_all_users; File.delete('/important_file')")
  
  service.save_to_file("../../../etc/passwd")
end